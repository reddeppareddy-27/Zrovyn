from rest_framework import permissions


class IsActive(permissions.BasePermission):
    """
    Permission to check if user is active and not suspended.
    """
    message = 'User account is inactive or suspended.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_active_user()


class IsViewerOrHigher(IsActive):
    """
    Permission for Viewer role or higher (Analyst, Admin).
    Allowed to view records and access summaries.
    """
    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return request.user.role and request.user.role.name in ['viewer', 'analyst', 'admin']


class IsAnalystOrHigher(IsActive):
    """
    Permission for Analyst role or higher (Admin).
    Allowed to view records, access insights, and manage analytics.
    """
    message = 'You must be an Analyst or higher to perform this action.'

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return request.user.role and request.user.role.name in ['analyst', 'admin']


class IsAdmin(IsActive):
    """
    Permission for Admin role only.
    Allowed to create, update, delete records, manage users, and all administrative actions.
    """
    message = 'You must be an Admin to perform this action.'

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return request.user.role and request.user.role.name == 'admin'


class IsOwnerOrAdmin(IsActive):
    """
    Permission for users to access their own records or for admins to access any record.
    """
    message = 'You do not have permission to access this record.'

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return True

    def has_object_permission(self, request, view, obj):
        """Check if user is the owner or admin."""
        if request.user.role and request.user.role.name == 'admin':
            return True
        return obj.user == request.user


class CanCreateRecords(IsAnalystOrHigher):
    """
    Permission to create financial records.
    Only Analyst and Admin can create records.
    """
    message = 'You must be an Analyst or higher to create records.'


class CanUpdateRecords(IsAnalystOrHigher):
    """
    Permission to update financial records.
    - Analyst: Can update their own records only
    - Admin: Can update any records
    - Viewer: Cannot update (read-only)
    """
    message = 'You do not have permission to update this record.'

    def has_object_permission(self, request, view, obj):
        """Check if user is analyst/admin and owner or admin."""
        if not super().has_permission(request, view):
            return False
        # Admin can update any record
        if request.user.role and request.user.role.name == 'admin':
            return True
        # Analyst can only update their own records
        return obj.user == request.user


class CanDeleteRecords(IsAdmin):
    """
    Permission to delete financial records.
    Only Admin can delete records.
    """
    message = 'You must be an Admin to delete records.'
