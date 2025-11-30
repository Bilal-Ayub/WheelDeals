from django import forms
from .models import InspectionRequest
from datetime import date, timedelta


class InspectionRequestForm(forms.ModelForm):
    """Form for buyers to request inspection"""

    class Meta:
        model = InspectionRequest
        fields = []  # Buyer just clicks button, no form fields needed


class AcceptInspectionForm(forms.ModelForm):
    """Form for sellers to accept inspection and schedule it"""

    scheduled_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        help_text="Select a date for the inspection",
    )

    class Meta:
        model = InspectionRequest
        fields = ["scheduled_date", "scheduled_time_slot"]
        widgets = {
            "scheduled_time_slot": forms.Select(attrs={"class": "form-control"}),
        }

    def clean_scheduled_date(self):
        scheduled_date = self.cleaned_data.get("scheduled_date")
        if scheduled_date and scheduled_date < date.today():
            raise forms.ValidationError("Inspection date cannot be in the past.")
        if scheduled_date and scheduled_date < date.today() + timedelta(days=1):
            raise forms.ValidationError("Please schedule at least 1 day in advance.")
        return scheduled_date


class RejectInspectionForm(forms.ModelForm):
    """Form for sellers to reject inspection request"""

    rejection_reason = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Please provide a reason for rejection (optional)",
            }
        ),
        required=False,
    )

    class Meta:
        model = InspectionRequest
        fields = ["rejection_reason"]


class InspectionReportForm(forms.ModelForm):
    """Form for inspectors to submit inspection reports"""

    class Meta:
        from .models import InspectionReport

        model = InspectionReport
        fields = [
            "paint_condition",
            "body_condition",
            "glass_windows",
            "lights_signals",
            "tire_condition",
            "wheel_condition",
            "engine_condition",
            "transmission",
            "brakes",
            "suspension",
            "interior_condition",
            "seats_upholstery",
            "dashboard_controls",
            "electronics",
            "overall_comments",
        ]
        widgets = {
            "paint_condition": forms.RadioSelect(attrs={"class": "form-check-input"}),
            "body_condition": forms.RadioSelect(attrs={"class": "form-check-input"}),
            "glass_windows": forms.RadioSelect(attrs={"class": "form-check-input"}),
            "lights_signals": forms.RadioSelect(attrs={"class": "form-check-input"}),
            "tire_condition": forms.RadioSelect(attrs={"class": "form-check-input"}),
            "wheel_condition": forms.RadioSelect(attrs={"class": "form-check-input"}),
            "engine_condition": forms.RadioSelect(attrs={"class": "form-check-input"}),
            "transmission": forms.RadioSelect(attrs={"class": "form-check-input"}),
            "brakes": forms.RadioSelect(attrs={"class": "form-check-input"}),
            "suspension": forms.RadioSelect(attrs={"class": "form-check-input"}),
            "interior_condition": forms.RadioSelect(
                attrs={"class": "form-check-input"}
            ),
            "seats_upholstery": forms.RadioSelect(attrs={"class": "form-check-input"}),
            "dashboard_controls": forms.RadioSelect(
                attrs={"class": "form-check-input"}
            ),
            "electronics": forms.RadioSelect(attrs={"class": "form-check-input"}),
            "overall_comments": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
        }
        labels = {
            "paint_condition": "Paint Condition",
            "body_condition": "Body Condition",
            "glass_windows": "Glass & Windows",
            "lights_signals": "Lights & Signals",
            "tire_condition": "Tire Condition",
            "wheel_condition": "Wheel/Rim Condition",
            "engine_condition": "Engine Condition",
            "transmission": "Transmission",
            "brakes": "Brake System",
            "suspension": "Suspension System",
            "interior_condition": "Interior Overall",
            "seats_upholstery": "Seats & Upholstery",
            "dashboard_controls": "Dashboard & Controls",
            "electronics": "Electronics & Features",
            "overall_comments": "Overall Comments & Notes",
        }


class InspectionPhotoForm(forms.ModelForm):
    """Form for uploading inspection photos"""

    class Meta:
        from .models import InspectionPhoto

        model = InspectionPhoto
        fields = ["image", "caption"]
        widgets = {
            "image": forms.FileInput(
                attrs={"class": "form-control", "accept": "image/*"}
            ),
            "caption": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Photo description (optional)",
                }
            ),
        }
