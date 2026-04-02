from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Role, FinancialRecord


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'status', 'id')}),
    )
    list_display = ['username', 'email', 'get_role_display', 'status', 'is_active', 'created_at']
    list_filter = ['role', 'status', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['id', 'created_at', 'updated_at']

    def get_role_display(self, obj):
        return obj.get_role_display()
    get_role_display.short_description = 'Role'


@admin.register(FinancialRecord)
class FinancialRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'record_type', 'category', 'date', 'is_deleted', 'created_at']
    list_filter = ['record_type', 'category', 'date', 'is_deleted', 'created_at']
    search_fields = ['user__username', 'description', 'category']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-date', '-created_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'amount', 'record_type', 'category')
        }),
        ('Details', {
            'fields': ('description', 'date')
        }),
        ('Status', {
            'fields': ('is_deleted',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Show all records including soft-deleted ones to admin."""
        return FinancialRecord.objects.all()
