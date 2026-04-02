#!/usr/bin/env python
"""
Setup initial roles and users for the Finance Backend
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_backend.settings')
django.setup()

from finance.models import Role, CustomUser
from rest_framework.authtoken.models import Token

def setup_data():
    print("=" * 60)
    print("Finance Backend - Initial Setup")
    print("=" * 60)
    
    # Create roles
    print("\n📝 Creating roles...")
    viewer_role, _ = Role.objects.get_or_create(
        name='viewer',
        defaults={'description': 'Read-only access to records and summaries'}
    )
    analyst_role, _ = Role.objects.get_or_create(
        name='analyst', 
        defaults={'description': 'Can view and analyze records, create own records'}
    )
    admin_role, _ = Role.objects.get_or_create(
        name='admin',
        defaults={'description': 'Full administrative access'}
    )
    print(f"✅ Roles created: viewer, analyst, admin")

    # Create users
    print("\n👤 Creating users...")

    # Admin user
    admin_user, created = CustomUser.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'role': admin_role,
            'status': 'active',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
    admin_token, _ = Token.objects.get_or_create(user=admin_user)
    print(f"✅ Admin User")
    print(f"   • Username: admin")
    print(f"   • Password: admin123")
    print(f"   • Token: {admin_token.key}")

    # Analyst user
    analyst_user, created = CustomUser.objects.get_or_create(
        username='analyst',
        defaults={
            'email': 'analyst@example.com',
            'role': analyst_role,
            'status': 'active',
        }
    )
    if created:
        analyst_user.set_password('analyst123')
        analyst_user.save()
    analyst_token, _ = Token.objects.get_or_create(user=analyst_user)
    print(f"\n✅ Analyst User")
    print(f"   • Username: analyst")
    print(f"   • Password: analyst123")
    print(f"   • Token: {analyst_token.key}")

    # Viewer user
    viewer_user, created = CustomUser.objects.get_or_create(
        username='viewer',
        defaults={
            'email': 'viewer@example.com',
            'role': viewer_role,
            'status': 'active',
        }
    )
    if created:
        viewer_user.set_password('viewer123')
        viewer_user.save()
    viewer_token, _ = Token.objects.get_or_create(user=viewer_user)
    print(f"\n✅ Viewer User")
    print(f"   • Username: viewer")
    print(f"   • Password: viewer123")
    print(f"   • Token: {viewer_token.key}")

    print("\n" + "=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    print("\n📚 API Documentation:")
    print("   • Root: http://localhost:8000/")
    print("   • API: http://localhost:8000/api/v1/")
    print("   • Admin: http://localhost:8000/admin/")
    print("\n🔗 Example API Request:")
    print(f"   curl -H 'Authorization: Token {analyst_token.key}' \\")
    print("     http://localhost:8000/api/v1/records/")

if __name__ == '__main__':
    setup_data()
