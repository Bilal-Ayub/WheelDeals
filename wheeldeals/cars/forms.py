from django import forms
from .models import Car


class CarForm(forms.ModelForm):
    """
    Form for adding and editing car listings.
    """

    class Meta:
        model = Car
        fields = [
            "make",
            "model",
            "year",
            "price",
            "mileage",
            "color",
            "transmission",
            "fuel_type",
            "description",
            "image1",
            "image2",
            "image3",
        ]
        widgets = {
            "make": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g., Toyota"}
            ),
            "model": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g., Corolla"}
            ),
            "year": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "2020"}
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "25000.00"}
            ),
            "mileage": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Kilometers"}
            ),
            "color": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g., Black"}
            ),
            "transmission": forms.Select(attrs={"class": "form-control"}),
            "fuel_type": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe your car...",
                }
            ),
            "image1": forms.FileInput(attrs={"class": "form-control"}),
            "image2": forms.FileInput(attrs={"class": "form-control"}),
            "image3": forms.FileInput(attrs={"class": "form-control"}),
        }


class CarSearchForm(forms.Form):
    """Form for searching cars"""

    query = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Search by make, model..."}
        ),
    )
    min_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Min Price"}
        ),
    )
    max_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Max Price"}
        ),
    )
    transmission = forms.ChoiceField(
        required=False,
        choices=[("", "Any")] + Car.TRANSMISSION_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    fuel_type = forms.ChoiceField(
        required=False,
        choices=[("", "Any")] + Car.FUEL_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
