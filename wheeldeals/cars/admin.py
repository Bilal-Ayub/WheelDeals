from django.contrib import admin
from .models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """Admin configuration for Car model"""

    list_display = [
        "make",
        "model",
        "year",
        "price",
        "seller",
        "date_posted",
        "is_sold",
        "views",
    ]
    list_filter = ["is_sold", "make", "fuel_type", "transmission", "year"]
    search_fields = ["make", "model", "description", "seller__username"]
    readonly_fields = ["date_posted", "views"]
    list_editable = ["is_sold"]

    fieldsets = (
        ("Basic Information", {"fields": ("make", "model", "year", "price")}),
        (
            "Specifications",
            {"fields": ("mileage", "color", "transmission", "fuel_type")},
        ),
        (
            "Description & Images",
            {"fields": ("description", "image1", "image2", "image3")},
        ),
        ("Seller & Status", {"fields": ("seller", "is_sold", "date_posted", "views")}),
    )
