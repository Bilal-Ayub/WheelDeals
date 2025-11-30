from django.db import models
from django.conf import settings
from cars.models import Car
from django.utils import timezone
from datetime import timedelta


class InspectionRequest(models.Model):
    """
    Model for vehicle inspection requests.
    Buyers can request inspections for cars, sellers accept/reject,
    and inspectors perform the inspection.
    """

    STATUS_CHOICES = [
        ("requested", "Requested"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("scheduled", "Scheduled"),
        ("assigned", "Assigned"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    TIME_SLOT_CHOICES = [
        ("08:00-10:00", "8:00 AM - 10:00 AM"),
        ("10:00-12:00", "10:00 AM - 12:00 PM"),
        ("12:00-14:00", "12:00 PM - 2:00 PM"),
        ("14:00-16:00", "2:00 PM - 4:00 PM"),
        ("16:00-18:00", "4:00 PM - 6:00 PM"),
    ]

    # Auto-generated inspection ID
    inspection_id = models.CharField(max_length=20, unique=True, editable=False)

    # Relationships
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="inspection_requests"
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="requested_inspections",
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_inspection_requests",
    )
    inspector = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_inspections",
    )

    # Status and dates
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default="requested"
    )
    requested_date = models.DateTimeField(auto_now_add=True)
    scheduled_date = models.DateField(null=True, blank=True)
    scheduled_time_slot = models.CharField(
        max_length=15, choices=TIME_SLOT_CHOICES, null=True, blank=True
    )

    # Payment
    inspection_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=50.00
    )
    payment_method = models.CharField(max_length=50, default="Cash on Delivery")

    # Rejection reason
    rejection_reason = models.TextField(blank=True, null=True)

    # Metadata
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "inspections_inspectionrequest"
        ordering = ["-requested_date"]
        verbose_name = "Inspection Request"
        verbose_name_plural = "Inspection Requests"

    def __str__(self):
        return f"{self.inspection_id} - {self.car} ({self.status})"

    def save(self, *args, **kwargs):
        # Generate inspection ID if not exists
        if not self.inspection_id:
            # Format: INS-YYYYMMDD-XXXXX
            timestamp = timezone.now().strftime("%Y%m%d")
            count = InspectionRequest.objects.filter(
                inspection_id__startswith=f"INS-{timestamp}"
            ).count()
            self.inspection_id = f"INS-{timestamp}-{count + 1:05d}"
        super().save(*args, **kwargs)

    @staticmethod
    def can_request_inspection(car, buyer):
        """
        Check if a buyer can request an inspection for this car.
        30-day cooldown rule: same buyer cannot request inspection for same car within 30 days.
        Returns True if buyer can request inspection, False otherwise.
        """
        # Check if there's any inspection request by this buyer for this car in the last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_request = InspectionRequest.objects.filter(
            car=car, buyer=buyer, requested_date__gte=thirty_days_ago
        ).exists()

        # Can request if no recent request exists
        return not recent_request

    def get_time_range(self):
        """Return human-readable time range"""
        if self.scheduled_time_slot:
            return dict(self.TIME_SLOT_CHOICES).get(self.scheduled_time_slot)
        return None


class InspectionReport(models.Model):
    """
    Inspector's detailed report for a vehicle inspection.
    Contains ratings (1-5) for 15 vehicle components and photos.
    """

    RATING_CHOICES = [
        (1, "1 - Poor"),
        (2, "2 - Fair"),
        (3, "3 - Good"),
        (4, "4 - Very Good"),
        (5, "5 - Excellent"),
    ]

    # Relationship to inspection request
    inspection_request = models.OneToOneField(
        InspectionRequest, on_delete=models.CASCADE, related_name="report"
    )

    # 14 Vehicle Components - Each rated 1-5
    # Exterior Components
    paint_condition = models.IntegerField(choices=RATING_CHOICES)
    body_condition = models.IntegerField(choices=RATING_CHOICES)
    glass_windows = models.IntegerField(choices=RATING_CHOICES)
    lights_signals = models.IntegerField(choices=RATING_CHOICES)

    # Tires & Wheels
    tire_condition = models.IntegerField(choices=RATING_CHOICES)
    wheel_condition = models.IntegerField(choices=RATING_CHOICES)

    # Mechanical Components
    engine_condition = models.IntegerField(choices=RATING_CHOICES)
    transmission = models.IntegerField(choices=RATING_CHOICES)
    brakes = models.IntegerField(choices=RATING_CHOICES)
    suspension = models.IntegerField(choices=RATING_CHOICES)

    # Interior Components
    interior_condition = models.IntegerField(choices=RATING_CHOICES)
    seats_upholstery = models.IntegerField(choices=RATING_CHOICES)
    dashboard_controls = models.IntegerField(choices=RATING_CHOICES)

    # Electronics & Features
    electronics = models.IntegerField(choices=RATING_CHOICES)

    # Additional notes
    overall_comments = models.TextField(blank=True, null=True)

    # Timestamps
    completed_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "inspections_inspectionreport"
        ordering = ["-completed_date"]
        verbose_name = "Inspection Report"
        verbose_name_plural = "Inspection Reports"

    def __str__(self):
        return f"Report for {self.inspection_request.inspection_id}"

    def average_rating(self):
        """Calculate average rating across all components"""
        ratings = [
            self.paint_condition,
            self.body_condition,
            self.glass_windows,
            self.lights_signals,
            self.tire_condition,
            self.wheel_condition,
            self.engine_condition,
            self.transmission,
            self.brakes,
            self.suspension,
            self.interior_condition,
            self.seats_upholstery,
            self.dashboard_controls,
            self.electronics,
        ]
        return sum(ratings) / len(ratings)


class InspectionPhoto(models.Model):
    """
    Photos uploaded by inspector as part of inspection report.
    """

    report = models.ForeignKey(
        InspectionReport, on_delete=models.CASCADE, related_name="photos"
    )
    image = models.ImageField(upload_to="inspection_photos/%Y/%m/%d/")
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "inspections_inspectionphoto"
        ordering = ["uploaded_at"]
        verbose_name = "Inspection Photo"
        verbose_name_plural = "Inspection Photos"

    def __str__(self):
        return f"Photo for {self.report.inspection_request.inspection_id}"
