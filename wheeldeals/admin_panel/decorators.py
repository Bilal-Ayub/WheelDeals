from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def admin_required(view_func):
    """
    Decorator to ensure only admin users can access certain views.
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to access this page.")
            return redirect("login")

        if not request.user.is_admin():
            messages.error(request, "You do not have permission to access this page.")
            return redirect("home")

        return view_func(request, *args, **kwargs)

    return wrapper
