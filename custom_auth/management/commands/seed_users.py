from django.core.management.base import BaseCommand
from custom_auth.models import CustomUser, ObjectPermission
from custom_auth.constants import ActionEnum


class Command(BaseCommand):
    help = "Seeds the database with an admin user and global permissions for Questions, along with 3-4 regular users."

    def handle(self, *args, **kwargs):
        # Admin credentials
        admin_email = "admin@gmail.com"
        admin_password = "admin"

        # Check if admin user already exists
        if not CustomUser.objects.filter(email=admin_email).exists():
            admin_user = CustomUser.objects.create_superuser(
                email=admin_email,
                username="admin",
                password=admin_password,
            )
            self.stdout.write(self.style.SUCCESS(f"Admin user created: {admin_email}"))

            # Grant global permissions for Questions
            actions = [ActionEnum.VIEW, ActionEnum.CREATE, ActionEnum.EDIT, ActionEnum.DELETE]
            for action in actions:
                ObjectPermission.objects.create(
                    user=admin_user,
                    action=action.value,
                    object_id=None
                )
            self.stdout.write(self.style.SUCCESS("Global permissions granted for Questions."))
        else:
            admin_user = CustomUser.objects.get(email=admin_email)
            self.stdout.write(self.style.WARNING("Admin user already exists."))

        # Create 3-4 non-admin users
        regular_users_data = [
            {"email": "user1@gmail.com", "username": "user1", "password": "user1pass"},
            {"email": "user2@gmail.com", "username": "user2", "password": "user2pass"},
            {"email": "user3@gmail.com", "username": "user3", "password": "user3pass"},
            {"email": "user4@gmail.com", "username": "user4", "password": "user4pass"},
        ]

        for user_data in regular_users_data:
            if not CustomUser.objects.filter(email=user_data["email"]).exists():
                CustomUser.objects.create_user(
                    email=user_data["email"],
                    username=user_data["username"],
                    password=user_data["password"],
                )
                self.stdout.write(self.style.SUCCESS(f"Regular user created: {user_data['email']}"))
            else:
                self.stdout.write(self.style.WARNING(f"User already exists: {user_data['email']}"))
