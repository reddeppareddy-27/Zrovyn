from django.contrib.auth import get_user_model
from finance.models import Role

User = get_user_model()

# Get or create admin role
admin_role, _ = Role.objects.get_or_create(
    name='admin',
    defaults={'description': 'Full administrative access'}
)

# Create admin user if it doesn't exist
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    admin_user.role = admin_role
    admin_user.status = 'active'
    admin_user.save()
    print("✅ Admin user created successfully!")
    print(f"   Username: admin")
    print(f"   Password: admin123")
else:
    print("✅ Admin user already exists")
