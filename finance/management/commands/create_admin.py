from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from finance.models import Role

User = get_user_model()


class Command(BaseCommand):
    help = 'Create initial admin user and roles'

    def handle(self, *args, **options):
        self.stdout.write("Creating roles...")
        
        # Create roles
        admin_role, _ = Role.objects.get_or_create(
            name='admin',
            defaults={'description': 'Full administrative access'}
        )
        analyst_role, _ = Role.objects.get_or_create(
            name='analyst',
            defaults={'description': 'Can view and analyze records'}
        )
        viewer_role, _ = Role.objects.get_or_create(
            name='viewer',
            defaults={'description': 'Read-only access'}
        )
        
        self.stdout.write(self.style.SUCCESS("✅ Roles created"))
        
        # Create admin user
        self.stdout.write("Creating admin user...")
        if not User.objects.filter(username='admin').exists():
            User.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='admin123',
                role=admin_role,
                status='active',
                is_staff=True,
                is_superuser=True,
            )
            self.stdout.write(self.style.SUCCESS("✅ Admin user created"))
            self.stdout.write(f"   Username: admin")
            self.stdout.write(f"   Password: admin123")
        else:
            self.stdout.write(self.style.WARNING("⚠️  Admin user already exists"))
