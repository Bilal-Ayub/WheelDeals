import uuid
from django.contrib.auth import login
from .models import CustomUser


def create_guest_user(request):
    """
    Create a guest user and log them in automatically.
    Guest users have a unique username and are marked as guests.
    """
    # Generate unique guest username
    guest_username = f"guest_{uuid.uuid4().hex[:12]}"

    # Create guest user with minimal information
    guest_user = CustomUser.objects.create_user(
        username=guest_username,
        password=uuid.uuid4().hex,  # Random password they'll never use
        is_guest=True,
        first_name="Guest",
        last_name="User",
    )

    # Log in the guest user
    login(request, guest_user, backend="django.contrib.auth.backends.ModelBackend")

    return guest_user


def is_guest_user(user):
    """
    Check if a user is a guest user.
    """
    return user.is_authenticated and hasattr(user, "is_guest") and user.is_guest
