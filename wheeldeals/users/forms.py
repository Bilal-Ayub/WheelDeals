from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Form for user registration.
    Extends Django's UserCreationForm to include our custom fields.
    """

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    phone = forms.CharField(max_length=15, required=False)
    city = forms.CharField(max_length=100, required=False)

    # Exclude 'admin' role from normal user signup
    SIGNUP_ROLE_CHOICES = [
        ("buyer", "Buyer"),
        ("seller", "Seller"),
        ("inspector", "Inspector"),
    ]

    role = forms.ChoiceField(
        choices=SIGNUP_ROLE_CHOICES,
        required=True,
        widget=forms.RadioSelect,
        initial="buyer",
        help_text="Select your role: Buyer (search and view ads) or Seller (post and manage ads)",
    )

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "city",
            "role",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            if field_name != "role":  # Skip role as it's radio buttons
                field.widget.attrs["class"] = "form-control"
            if field_name == "username":
                field.widget.attrs["placeholder"] = "Choose a username"
            elif field_name == "email":
                field.widget.attrs["placeholder"] = "your.email@example.com"
            elif field_name == "first_name":
                field.widget.attrs["placeholder"] = "First Name"
            elif field_name == "last_name":
                field.widget.attrs["placeholder"] = "Last Name"
            elif field_name == "phone":
                field.widget.attrs["placeholder"] = "Phone Number"
            elif field_name == "city":
                field.widget.attrs["placeholder"] = "City"
            elif field_name == "password1":
                field.widget.attrs["placeholder"] = "Password"
            elif field_name == "password2":
                field.widget.attrs["placeholder"] = "Confirm Password"


class CustomUserUpdateForm(UserChangeForm):
    """
    Form for updating user profile.
    Allows users to edit their information.
    """

    password = None  # Remove password field from this form

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "phone", "city")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
