from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta

from .models import CustomUser, Role, FinancialRecord
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    RoleSerializer, FinancialRecordSerializer, FinancialRecordCreateUpdateSerializer,
    DashboardSummarySerializer, CategorySummarySerializer, MonthlySummarySerializer,
    RecentActivitySerializer
)
from .permissions import (
    IsViewerOrHigher, IsAnalystOrHigher, IsAdmin, IsOwnerOrAdmin,
    CanCreateRecords, CanUpdateRecords, CanDeleteRecords, IsActive
)
from .services import FinancialSummaryService


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination for list views."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing roles.
    Provides read-only access to available roles.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsActive]
    pagination_class = StandardResultsSetPagination


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users.
    - Admin: Can list, create, update, delete any user
    - Analyst: Can view user list and own profile
    - Viewer: Can only view own profile
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['created_at', 'username']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Return queryset based on user role.
        - Admin: all users
        - Others: only themselves
        """
        if self.request.user.role and self.request.user.role.name == 'admin':
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)

    def get_serializer_class(self):
        """Use different serializers for different actions."""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == 'create':
            return [IsAdmin()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        elif self.action == 'list':
            return [IsAnalystOrHigher()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'], permission_classes=[IsActive])
    def me(self, request):
        """Get current user's profile."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdmin()])
    def inactive_users(self, request):
        """Get list of inactive users (Admin only)."""
        inactive = CustomUser.objects.filter(status__in=['inactive', 'suspended'])
        paginated = self.paginate_queryset(inactive)
        serializer = self.get_serializer(paginated, many=True)
        return self.get_paginated_response(serializer.data)


class FinancialRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing financial records.
    - Admin: Full access to all user records
    - Analyst: Can create, read, update own records
    - Viewer: Can only view own records (read-only)
    """
    serializer_class = FinancialRecordSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['category', 'description']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date', '-created_at']

    def get_queryset(self):
        """
        Return queries based on user role.
        - Admin: all records
        - Analyst/Viewer: only their own records
        """
        user = self.request.user
        if user.role and user.role.name == 'admin':
            queryset = FinancialRecord.objects.filter(is_deleted=False)
        else:
            queryset = FinancialRecord.objects.filter(user=user, is_deleted=False)

        # Filter by date range if provided
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__gte=start_date)
            except ValueError:
                pass

        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__lte=end_date)
            except ValueError:
                pass

        # Filter by type if provided
        record_type = self.request.query_params.get('type')
        if record_type in ['income', 'expense']:
            queryset = queryset.filter(record_type=record_type)

        # Filter by category if provided
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        return queryset

    def get_serializer_class(self):
        """Use different serializers for different actions."""
        if self.action in ['create', 'update', 'partial_update']:
            return FinancialRecordCreateUpdateSerializer
        return FinancialRecordSerializer

    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == 'create':
            return [CanCreateRecords()]
        elif self.action in ['update', 'partial_update']:
            return [CanUpdateRecords()]
        elif self.action == 'destroy':
            return [CanDeleteRecords()]
        elif self.action == 'list':
            return [IsViewerOrHigher()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """Automatically set the user to the current user."""
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        """Soft delete the record."""
        instance.is_deleted = True
        instance.save()

    @action(detail=False, methods=['get'], permission_classes=[IsViewerOrHigher()])
    def summary(self, request):
        """Get dashboard summary for the user."""
        summary_data = FinancialSummaryService.get_dashboard_summary(request.user)
        serializer = DashboardSummarySerializer(summary_data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsViewerOrHigher()])
    def category_summary(self, request):
        """Get summary grouped by category."""
        summary_data = FinancialSummaryService.get_category_summary(request.user)
        page = self.paginate_queryset(summary_data)
        serializer = CategorySummarySerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsViewerOrHigher()])
    def monthly_summary(self, request):
        """Get monthly summary for the past N months."""
        months = int(request.query_params.get('months', 12))
        summary_data = FinancialSummaryService.get_monthly_summary(request.user, months=months)
        serializer = MonthlySummarySerializer(summary_data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsViewerOrHigher()])
    def recent_activity(self, request):
        """Get recent financial activity."""
        limit = int(request.query_params.get('limit', 10))
        activity_data = FinancialSummaryService.get_recent_activity(request.user, limit=limit)
        serializer = RecentActivitySerializer(activity_data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsViewerOrHigher()])
    def statistics(self, request):
        """Get statistics for a specific date range."""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response(
                {'error': 'start_date and end_date query parameters are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Dates must be in YYYY-MM-DD format.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if start_date > end_date:
            return Response(
                {'error': 'start_date cannot be after end_date.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        stats = FinancialSummaryService.get_record_statistics_for_period(
            request.user, start_date, end_date
        )
        return Response(stats)

    @action(detail=False, methods=['post'], permission_classes=[IsAnalystOrHigher()])
    def bulk_create(self, request):
        """
        Create multiple financial records at once.
        Expects a list of record data in the request body.
        """
        records_data = request.data if isinstance(request.data, list) else request.data.get('records', [])

        if not isinstance(records_data, list):
            return Response(
                {'error': 'Records must be provided as a list.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        created_records = []
        errors = []

        for idx, record_data in enumerate(records_data):
            serializer = FinancialRecordCreateUpdateSerializer(data=record_data)
            if serializer.is_valid():
                record = serializer.save(user=request.user)
                created_records.append(FinancialRecordSerializer(record).data)
            else:
                errors.append({'index': idx, 'errors': serializer.errors})

        response_data = {
            'created_count': len(created_records),
            'error_count': len(errors),
            'created_records': created_records,
        }

        if errors:
            response_data['errors'] = errors

        return Response(response_data, status=status.HTTP_201_CREATED if not errors else status.HTTP_207_MULTI_STATUS)


class DashboardViewSet(viewsets.ViewSet):
    """
    ViewSet for dashboard-specific endpoints.
    Provides aggregated data and analytics for the dashboard.
    """
    permission_classes = [IsViewerOrHigher()]

    @action(detail=False, methods=['get'], url_path='overview')
    def overview(self, request):
        """
        Get comprehensive dashboard overview.
        Includes summary, recent activity, and monthly trends.
        """
        summary = FinancialSummaryService.get_dashboard_summary(request.user)
        recent = FinancialSummaryService.get_recent_activity(request.user, limit=5)
        monthly = FinancialSummaryService.get_monthly_summary(request.user, months=6)

        response_data = {
            'summary': summary,
            'recent_activity': recent,
            'monthly_trends': monthly,
        }

        return Response(response_data)

    @action(detail=False, methods=['get'], url_path='insights')
    def insights(self, request):
        """
        Get financial insights and analytics.
        """
        summary = FinancialSummaryService.get_dashboard_summary(request.user)
        category_summary = FinancialSummaryService.get_category_summary(request.user)

        # Calculate some insights
        if summary['total_records'] > 0:
            avg_transaction = (summary['total_income'] + summary['total_expenses']) / summary['total_records']
        else:
            avg_transaction = 0

        top_category = max(category_summary, key=lambda x: x['total_amount']) if category_summary else None

        insights = {
            'net_balance': summary['net_balance'],
            'income_to_expense_ratio': summary['total_income'] / summary['total_expenses'] if summary['total_expenses'] > 0 else 0,
            'average_transaction': avg_transaction,
            'top_category': top_category,
            'total_transactions': summary['total_records'],
        }

        return Response(insights)
