from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from finance.models import Role

User = get_user_model()


class Command(BaseCommand):
    help = 'Create initial admin user and roles'

    def handle(self, *args, **options):
        try:
            self.stdout.write("Creating roles...")
            
            # Create roles first
            admin_role, created = Role.objects.get_or_create(
                name='admin',
                defaults={'description': 'Full administrative access'}
            )
            if created:
                self.stdout.write(self.style.SUCCESS("✅ Created admin role"))
            else:
                self.stdout.write(self.style.WARNING("⚠️  Admin role already exists"))
            
            analyst_role, created = Role.objects.get_or_create(
                name='analyst',
                defaults={'description': 'Can view and analyze records'}
            )
            viewer_role, created = Role.objects.get_or_create(
                name='viewer',
                defaults={'description': 'Read-only access'}
            )
            
            self.stdout.write(self.style.SUCCESS("✅ All roles ready"))
            
            # Create admin user
            self.stdout.write("Creating admin user...")
            if not User.objects.filter(username='admin').exists():
                admin_user = User.objects.create_user(
                    username='admin',
                    email='admin@example.com',
                    password='admin123',
                    role=admin_role,
                    status='active',
                    is_staff=True,
                    is_superuser=True,
                )
                self.stdout.write(self.style.SUCCESS("✅ Admin user created successfully!"))
                self.stdout.write(f"   • Username: admin")
                self.stdout.write(f"   • Password: admin123")
                self.stdout.write(f"   • Email: admin@example.com")
            else:
                # Update existing admin user
                admin_user = User.objects.get(username='admin')
                admin_user.is_staff = True
                admin_user.is_superuser = True
                admin_user.role = admin_role
                admin_user.status = 'active'
                admin_user.save()
                self.stdout.write(self.style.WARNING("⚠️  Admin user already exists - updated permissions"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {str(e)}"))
            import traceback
            self.stdout.write(traceback.format_exc())
