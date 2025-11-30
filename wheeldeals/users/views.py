from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .utils import create_guest_user, is_guest_user


def register(request):
    """
    User registration view.

    SQL Query executed by Django ORM:
    INSERT INTO users_customuser (username, email, password, first_name,
                                   last_name, phone, city, is_staff,
                                   is_active, is_superuser, date_joined)
    VALUES (?, ?, ?, ?, ?, ?, ?, 0, 1, 0, CURRENT_TIMESTAMP);
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Account created for {username}! You can now log in."
            )
            return redirect("login")
    else:
        form = CustomUserCreationForm()

    return render(request, "users/register.html", {"form": form})


def user_login(request):
    """
    User login view.

    SQL Query executed by Django ORM:
    SELECT id, username, password, email, first_name, last_name, phone, city
    FROM users_customuser
    WHERE username = ? AND is_active = 1;
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "users/login.html", {"form": form})


def user_logout(request):
    """User logout view"""
    # If it's a guest user, delete the account
    if request.user.is_authenticated and is_guest_user(request.user):
        guest_user = request.user
        logout(request)
        guest_user.delete()  # Delete guest user after logout
        messages.info(request, "Guest session ended.")
    else:
        logout(request)
        messages.info(request, "You have been logged out.")
    return redirect("home")


def continue_as_guest(request):
    """
    Create a guest user and log them in.
    Redirects to home page.
    """
    if not request.user.is_authenticated:
        create_guest_user(request)
        messages.info(
            request, "You are browsing as a guest. Contact information will be hidden."
        )
    return redirect("home")


@login_required
def profile(request):
    """
    User profile view - displays and allows editing of user information.
    Guest users are redirected to register page.

    SQL Query to get user data:
    SELECT * FROM users_customuser WHERE id = ?;

    SQL Query to update (when form is submitted):
    UPDATE users_customuser
    SET first_name = ?, last_name = ?, email = ?, phone = ?, city = ?
    WHERE id = ?;
    """
    # Redirect guest users to register page
    if is_guest_user(request.user):
        messages.warning(request, "Please sign up to access your profile.")
        return redirect("register")

    if request.method == "POST":
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("profile")
    else:
        form = CustomUserUpdateForm(instance=request.user)

    # Get user's cars
    # SQL: SELECT * FROM cars_car WHERE seller_id = ? ORDER BY date_posted DESC;
    user_cars = request.user.cars.all()

    context = {"form": form, "user_cars": user_cars}
    return render(request, "users/profile.html", context)
