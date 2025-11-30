from django.contrib import admin
from .models import InspectionRequest, InspectionReport, InspectionPhoto


@admin.register(InspectionRequest)
class InspectionRequestAdmin(admin.ModelAdmin):
    list_display = (
        "inspection_id",
        "car",
        "buyer",
        "seller",
        "inspector",
        "status",
        "requested_date",
        "scheduled_date",
    )
    list_filter = ("status", "requested_date", "scheduled_date")
    search_fields = ("inspection_id", "car__make", "car__model", "buyer__username")
    readonly_fields = ("inspection_id", "requested_date", "updated_at")

    fieldsets = (
        ("Inspection Info", {"fields": ("inspection_id", "car", "status")}),
        ("Parties", {"fields": ("buyer", "seller", "inspector")}),
        (
            "Schedule",
            {"fields": ("requested_date", "scheduled_date", "scheduled_time_slot")},
        ),
        ("Payment", {"fields": ("inspection_cost", "payment_method")}),
        ("Additional Info", {"fields": ("rejection_reason", "updated_at")}),
    )


class InspectionPhotoInline(admin.TabularInline):
    model = InspectionPhoto
    extra = 1
    fields = ("image", "caption", "uploaded_at")
    readonly_fields = ("uploaded_at",)


@admin.register(InspectionReport)
class InspectionReportAdmin(admin.ModelAdmin):
    list_display = (
        "inspection_request",
        "average_rating",
        "completed_date",
    )
    list_filter = ("completed_date",)
    search_fields = ("inspection_request__inspection_id",)
    readonly_fields = ("completed_date", "updated_at")
    inlines = [InspectionPhotoInline]

    fieldsets = (
        (
            "Inspection Info",
            {"fields": ("inspection_request", "completed_date", "updated_at")},
        ),
        (
            "Exterior Components",
            {
                "fields": (
                    "paint_condition",
                    "body_condition",
                    "glass_windows",
                    "lights_signals",
                )
            },
        ),
        ("Tires & Wheels", {"fields": ("tire_condition", "wheel_condition")}),
        (
            "Mechanical Components",
            {
                "fields": (
                    "engine_condition",
                    "transmission",
                    "brakes",
                    "suspension",
                )
            },
        ),
        (
            "Interior Components",
            {
                "fields": (
                    "interior_condition",
                    "seats_upholstery",
                    "dashboard_controls",
                )
            },
        ),
        ("Electronics & Features", {"fields": ("electronics",)}),
        (
            "Summary",
            {"fields": ("overall_comments",)},
        ),
    )


@admin.register(InspectionPhoto)
class InspectionPhotoAdmin(admin.ModelAdmin):
    list_display = ("report", "caption", "uploaded_at")
    list_filter = ("uploaded_at",)
    readonly_fields = ("uploaded_at",)
