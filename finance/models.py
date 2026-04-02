from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid


class Role(models.Model):
    """
    Custom role model for finer control over permissions.
    """
    ROLE_CHOICES = [
        ('viewer', 'Viewer'),
        ('analyst', 'Analyst'),
        ('admin', 'Admin'),
    ]

    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.get_name_display()


class CustomUser(AbstractUser):
    """
    Extended user model with role and status management.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='users')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def get_role_display(self):
        """Return the display name of the role."""
        return self.role.get_name_display() if self.role else 'No Role'

    def is_active_user(self):
        """Check if user is active."""
        return self.status == 'active' and self.is_active


class FinancialRecord(models.Model):
    """
    Model representing financial transactions or entries.
    """
    RECORD_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    CATEGORY_CHOICES = [
        ('salary', 'Salary'),
        ('bonus', 'Bonus'),
        ('investment', 'Investment'),
        ('food', 'Food'),
        ('transport', 'Transport'),
        ('utilities', 'Utilities'),
        ('entertainment', 'Entertainment'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='financial_records')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)  # Soft delete

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Financial Record'
        verbose_name_plural = 'Financial Records'
        indexes = [
            models.Index(fields=['user', '-date']),
            models.Index(fields=['user', 'record_type']),
            models.Index(fields=['user', 'category']),
            models.Index(fields=['is_deleted']),
        ]

    def __str__(self):
        return f"{self.get_record_type_display()}: ${self.amount} on {self.date}"

    def clean(self):
        """Validate the financial record."""
        if self.amount <= 0:
            raise ValidationError('Amount must be greater than 0.')
        if self.date > timezone.now().date():
            raise ValidationError('Date cannot be in the future.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
