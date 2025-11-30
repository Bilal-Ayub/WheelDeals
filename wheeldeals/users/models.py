from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    This allows us to add additional fields to the user model.

    SQL Query to create this table:
    CREATE TABLE users_customuser (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        password VARCHAR(128) NOT NULL,
        last_login DATETIME,
        is_superuser BOOL NOT NULL,
        username VARCHAR(150) UNIQUE NOT NULL,
        first_name VARCHAR(150) NOT NULL,
        last_name VARCHAR(150) NOT NULL,
        email VARCHAR(254) NOT NULL,
        is_staff BOOL NOT NULL,
        is_active BOOL NOT NULL,
        date_joined DATETIME NOT NULL,
        phone VARCHAR(15),
        city VARCHAR(100),
        is_guest BOOL NOT NULL DEFAULT 0,
        role VARCHAR(10) NOT NULL DEFAULT 'buyer'
    );
    """

    ROLE_CHOICES = [
        ("buyer", "Buyer"),
        ("seller", "Seller"),
        ("inspector", "Inspector"),
        ("admin", "Admin"),
    ]

    phone = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    is_guest = models.BooleanField(default=False, help_text="Is this a guest user?")
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="buyer",
        help_text="User role: Buyer can search/view ads, Seller can post/manage ads, Inspector can perform vehicle inspections",
    )

    def __str__(self):
        return self.username

    def is_buyer(self):
        """Check if user is a buyer"""
        return self.role == "buyer"

    def is_seller(self):
        """Check if user is a seller"""
        return self.role == "seller"

    def is_inspector(self):
        """Check if user is an inspector"""
        return self.role == "inspector"

    def is_admin(self):
        """Check if user is an admin"""
        return self.role == "admin"

    class Meta:
        db_table = "users_customuser"
        verbose_name = "User"
        verbose_name_plural = "Users"
