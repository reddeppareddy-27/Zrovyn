import pytest
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, timedelta
from decimal import Decimal

from finance.models import CustomUser, Role, FinancialRecord
from finance.services import FinancialSummaryService


class RoleTestCase(TestCase):
    """Test cases for Role model."""

    def setUp(self):
        """Set up test roles."""
        self.viewer_role = Role.objects.create(
            name='viewer',
            description='Read-only access'
        )
        self.analyst_role = Role.objects.create(
            name='analyst',
            description='Can view and analyze'
        )
        self.admin_role = Role.objects.create(
            name='admin',
            description='Full access'
        )

    def test_role_creation(self):
        """Test creating roles."""
        self.assertEqual(Role.objects.count(), 3)
        self.assertEqual(self.viewer_role.name, 'viewer')

    def test_role_display_name(self):
        """Test role display name."""
        self.assertEqual(self.viewer_role.get_name_display(), 'Viewer')
        self.assertEqual(self.analyst_role.get_name_display(), 'Analyst')
        self.assertEqual(self.admin_role.get_name_display(), 'Admin')


class CustomUserTestCase(TestCase):
    """Test cases for CustomUser model."""

    def setUp(self):
        """Set up test users."""
        self.admin_role = Role.objects.create(name='admin')
        self.analyst_role = Role.objects.create(name='analyst')

        self.admin_user = CustomUser.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpass123',
            role=self.admin_role
        )

        self.analyst_user = CustomUser.objects.create_user(
            username='analyst',
            email='analyst@example.com',
            password='testpass123',
            role=self.analyst_role
        )

    def test_user_creation(self):
        """Test creating users."""
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(self.admin_user.username, 'admin')

    def test_user_status(self):
        """Test user status."""
        self.assertEqual(self.admin_user.status, 'active')
        self.assertTrue(self.admin_user.is_active_user())

    def test_user_inactivation(self):
        """Test inactivating a user."""
        self.analyst_user.status = 'inactive'
        self.analyst_user.save()
        self.assertFalse(self.analyst_user.is_active_user())

    def test_user_role_display(self):
        """Test user role display."""
        self.assertEqual(self.admin_user.get_role_display(), 'Admin')
        self.assertEqual(self.analyst_user.get_role_display(), 'Analyst')


class FinancialRecordTestCase(TestCase):
    """Test cases for FinancialRecord model."""

    def setUp(self):
        """Set up test data."""
        self.admin_role = Role.objects.create(name='admin')
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role=self.admin_role
        )

    def test_income_record_creation(self):
        """Test creating an income record."""
        record = FinancialRecord.objects.create(
            user=self.user,
            amount=Decimal('5000.00'),
            record_type='income',
            category='salary',
            date=timezone.now().date()
        )
        self.assertEqual(record.amount, Decimal('5000.00'))
        self.assertEqual(record.record_type, 'income')

    def test_expense_record_creation(self):
        """Test creating an expense record."""
        record = FinancialRecord.objects.create(
            user=self.user,
            amount=Decimal('150.50'),
            record_type='expense',
            category='food',
            date=timezone.now().date()
        )
        self.assertEqual(record.amount, Decimal('150.50'))
        self.assertEqual(record.record_type, 'expense')

    def test_record_validation_negative_amount(self):
        """Test that negative amounts are rejected."""
        from django.core.exceptions import ValidationError
        record = FinancialRecord(
            user=self.user,
            amount=Decimal('-100.00'),
            record_type='income',
            category='salary',
            date=timezone.now().date()
        )
        with self.assertRaises(ValidationError):
            record.clean()

    def test_record_validation_future_date(self):
        """Test that future dates are rejected."""
        from django.core.exceptions import ValidationError
        record = FinancialRecord(
            user=self.user,
            amount=Decimal('100.00'),
            record_type='income',
            category='salary',
            date=timezone.now().date() + timedelta(days=1)
        )
        with self.assertRaises(ValidationError):
            record.clean()

    def test_soft_delete(self):
        """Test soft delete functionality."""
        record = FinancialRecord.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            record_type='income',
            category='salary',
            date=timezone.now().date()
        )
        record.is_deleted = True
        record.save()
        
        self.assertTrue(record.is_deleted)
        self.assertEqual(FinancialRecord.objects.filter(is_deleted=False).count(), 0)


class FinancialSummaryServiceTestCase(TestCase):
    """Test cases for FinancialSummaryService."""

    def setUp(self):
        """Set up test data."""
        self.admin_role = Role.objects.create(name='admin')
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role=self.admin_role
        )

        # Create some test records
        today = timezone.now().date()
        FinancialRecord.objects.create(
            user=self.user,
            amount=Decimal('5000.00'),
            record_type='income',
            category='salary',
            date=today
        )
        FinancialRecord.objects.create(
            user=self.user,
            amount=Decimal('1000.00'),
            record_type='expense',
            category='food',
            date=today
        )
        FinancialRecord.objects.create(
            user=self.user,
            amount=Decimal('500.00'),
            record_type='expense',
            category='transport',
            date=today
        )

    def test_dashboard_summary(self):
        """Test dashboard summary calculation."""
        summary = FinancialSummaryService.get_dashboard_summary(self.user)
        
        self.assertEqual(summary['total_income'], Decimal('5000.00'))
        self.assertEqual(summary['total_expenses'], Decimal('1500.00'))
        self.assertEqual(summary['net_balance'], Decimal('3500.00'))
        self.assertEqual(summary['total_records'], 3)

    def test_category_summary(self):
        """Test category-wise summary."""
        summary = FinancialSummaryService.get_category_summary(self.user)
        
        self.assertEqual(len(summary), 3)
        # Check that data is present
        categories = [item['category'] for item in summary]
        self.assertIn('salary', categories)
        self.assertIn('food', categories)
        self.assertIn('transport', categories)

    def test_monthly_summary(self):
        """Test monthly summary."""
        summary = FinancialSummaryService.get_monthly_summary(self.user, months=1)
        
        self.assertGreater(len(summary), 0)
        current = summary[-1]  # Last month
        self.assertEqual(current['income'], Decimal('5000.00'))
        self.assertEqual(current['expenses'], Decimal('1500.00'))

    def test_recent_activity(self):
        """Test recent activity retrieval."""
        activity = FinancialSummaryService.get_recent_activity(self.user, limit=2)
        
        self.assertEqual(len(activity), 2)
        self.assertIn('id', activity[0])
        self.assertIn('amount', activity[0])


class APIAuthenticationTestCase(TestCase):
    """Test cases for API authentication and authorization."""

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        self.viewer_role = Role.objects.create(name='viewer')
        self.analyst_role = Role.objects.create(name='analyst')
        self.admin_role = Role.objects.create(name='admin')

        self.viewer = CustomUser.objects.create_user(
            username='viewer',
            email='viewer@example.com',
            password='testpass123',
            role=self.viewer_role
        )

        self.analyst = CustomUser.objects.create_user(
            username='analyst',
            email='analyst@example.com',
            password='testpass123',
            role=self.analyst_role
        )

        self.admin = CustomUser.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpass123',
            role=self.admin_role
        )

    def test_unauthenticated_access_denied(self):
        """Test that unauthenticated requests are denied."""
        response = self.client.get('/api/v1/records/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_access_allowed(self):
        """Test that authenticated requests are allowed."""
        self.client.force_authenticate(user=self.viewer)
        response = self.client.get('/api/v1/records/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RecordPermissionTestCase(TestCase):
    """Test cases for financial record permissions."""

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        self.viewer_role = Role.objects.create(name='viewer')
        self.analyst_role = Role.objects.create(name='analyst')
        self.admin_role = Role.objects.create(name='admin')

        self.viewer = CustomUser.objects.create_user(
            username='viewer',
            email='viewer@example.com',
            password='testpass123',
            role=self.viewer_role
        )

        self.analyst = CustomUser.objects.create_user(
            username='analyst',
            email='analyst@example.com',
            password='testpass123',
            role=self.analyst_role
        )

        self.admin = CustomUser.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpass123',
            role=self.admin_role
        )

        # Create test records
        self.record_data = {
            'amount': '1000.00',
            'record_type': 'income',
            'category': 'salary',
            'date': timezone.now().date().isoformat(),
            'description': 'Test income'
        }

    def test_viewer_cannot_create_record(self):
        """Test that viewers cannot create records."""
        self.client.force_authenticate(user=self.viewer)
        response = self.client.post('/api/v1/records/', self.record_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_analyst_can_create_record(self):
        """Test that analysts can create records."""
        self.client.force_authenticate(user=self.analyst)
        response = self.client.post('/api/v1/records/', self.record_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_create_record(self):
        """Test that admins can create records."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/v1/records/', self.record_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
