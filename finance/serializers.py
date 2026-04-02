from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, Role, FinancialRecord
from decimal import Decimal


class RoleSerializer(serializers.ModelSerializer):
    """Serializer for Role model."""

    class Meta:
        model = Role
        fields = ['name', 'description', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser model. Used for listing and retrieving users."""
    role = serializers.StringRelatedField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'status',
                  'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'role', 'status']

    def validate(self, attrs):
        """Validate passwords match."""
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({'password': "Passwords don't match."})
        return attrs

    def create(self, validated_data):
        """Create user with hashed password."""
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data['role'],
            status=validated_data.get('status', 'active'),
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user information."""
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'role', 'status']


class FinancialRecordSerializer(serializers.ModelSerializer):
    """Serializer for FinancialRecord model."""
    user_username = serializers.CharField(source='user.username', read_only=True)
    record_type_display = serializers.CharField(source='get_record_type_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = FinancialRecord
        fields = ['id', 'user_username', 'amount', 'record_type', 'record_type_display',
                  'category', 'category_display', 'description', 'date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user_username', 'created_at', 'updated_at']


class FinancialRecordCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating financial records."""

    class Meta:
        model = FinancialRecord
        fields = ['amount', 'record_type', 'category', 'description', 'date']

    def validate_amount(self, value):
        """Validate amount is positive."""
        if value <= 0:
            raise serializers.ValidationError('Amount must be greater than 0.')
        return value


class DashboardSummarySerializer(serializers.Serializer):
    """Serializer for dashboard summary data."""
    total_income = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=15, decimal_places=2)
    net_balance = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_records = serializers.IntegerField()
    records_count_by_type = serializers.DictField()
    records_count_by_category = serializers.DictField()


class CategorySummarySerializer(serializers.Serializer):
    """Serializer for category-wise summary."""
    category = serializers.CharField()
    category_display = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    count = serializers.IntegerField()
    type = serializers.CharField()


class MonthlySummarySerializer(serializers.Serializer):
    """Serializer for monthly summary data."""
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    income = serializers.DecimalField(max_digits=15, decimal_places=2)
    expenses = serializers.DecimalField(max_digits=15, decimal_places=2)
    net = serializers.DecimalField(max_digits=15, decimal_places=2)


class RecentActivitySerializer(serializers.Serializer):
    """Serializer for recent activity on dashboard."""
    id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    record_type = serializers.CharField()
    category = serializers.CharField()
    description = serializers.CharField()
    date = serializers.DateField()
    created_at = serializers.DateTimeField()
