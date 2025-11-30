"""
Quick script to create an admin user for WheelDeals.
Run this after activating the virtual environment.

Usage:
    python create_admin.py
"""

import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wheeldeals_project.settings")
django.setup()

from users.models import CustomUser


def create_admin():
    """Create an admin user for testing."""

    username = input("Enter admin username (default: admin): ").strip() or "admin"
    email = (
        input("Enter admin email (default: admin@wheeldeals.com): ").strip()
        or "admin@wheeldeals.com"
    )
    password = input("Enter admin password (default: admin123): ").strip() or "admin123"
    first_name = input("Enter first name (default: Admin): ").strip() or "Admin"
    last_name = input("Enter last name (default: User): ").strip() or "User"

    # Check if user already exists
    if CustomUser.objects.filter(username=username).exists():
        print(f"\n❌ Error: User '{username}' already exists!")
        update = (
            input("Would you like to update this user to admin role? (y/n): ")
            .strip()
            .lower()
        )
        if update == "y":
            user = CustomUser.objects.get(username=username)
            user.role = "admin"
            user.save()
            print(f"✅ User '{username}' updated to admin role!")
        return

    # Create admin user
    try:
        admin = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role="admin",
        )

        print(f"\n✅ Admin user created successfully!")
        print(f"   Username: {admin.username}")
        print(f"   Email: {admin.email}")
        print(f"   Role: {admin.get_role_display()}")
        print(f"\n📌 Login at: http://127.0.0.1:8000/users/login/")
        print(f"📌 Admin Panel: http://127.0.0.1:8000/admin-panel/")

    except Exception as e:
        print(f"\n❌ Error creating admin user: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("WheelDeals Admin User Creation")
    print("=" * 60)
    print()
    create_admin()
    print()
    print("=" * 60)
