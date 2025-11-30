from django.db import models
from django.conf import settings
from django.utils import timezone


class Car(models.Model):
    """
    Car model for vehicle listings.

    SQL Query to create this table:
    CREATE TABLE cars_car (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        make VARCHAR(100) NOT NULL,
        model VARCHAR(100) NOT NULL,
        year INTEGER NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        mileage INTEGER,
        color VARCHAR(50),
        transmission VARCHAR(20),
        fuel_type VARCHAR(20),
        description TEXT,
        image1 VARCHAR(100),
        image2 VARCHAR(100),
        image3 VARCHAR(100),
        seller_id INTEGER NOT NULL,
        date_posted DATETIME NOT NULL,
        is_sold BOOL NOT NULL DEFAULT 0,
        views INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (seller_id) REFERENCES users_customuser(id)
    );

    SQL Queries for this model:

    1. Get all available cars (not sold):
    SELECT * FROM cars_car WHERE is_sold = 0 ORDER BY date_posted DESC;

    2. Get car details by ID:
    SELECT c.*, u.username, u.email, u.phone
    FROM cars_car c
    JOIN users_customuser u ON c.seller_id = u.id
    WHERE c.id = ?;

    3. Search cars by make and model:
    SELECT * FROM cars_car
    WHERE make LIKE '%?%' AND model LIKE '%?%' AND is_sold = 0;

    4. Get cars by price range:
    SELECT * FROM cars_car
    WHERE price BETWEEN ? AND ? AND is_sold = 0
    ORDER BY price ASC;
    """

    TRANSMISSION_CHOICES = [
        ("automatic", "Automatic"),
        ("manual", "Manual"),
    ]

    FUEL_CHOICES = [
        ("petrol", "Petrol"),
        ("diesel", "Diesel"),
        ("electric", "Electric"),
        ("hybrid", "Hybrid"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending Review"),
        ("published", "Published"),
        ("declined", "Declined"),
    ]

    # Basic Information
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Specifications
    mileage = models.IntegerField(
        null=True, blank=True, help_text="Mileage in kilometers"
    )
    color = models.CharField(max_length=50, blank=True)
    transmission = models.CharField(
        max_length=20, choices=TRANSMISSION_CHOICES, default="automatic"
    )
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default="petrol")

    # Description
    description = models.TextField(blank=True)

    # Images
    image1 = models.ImageField(upload_to="cars/", null=True, blank=True)
    image2 = models.ImageField(upload_to="cars/", null=True, blank=True)
    image3 = models.ImageField(upload_to="cars/", null=True, blank=True)

    # Relationships
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cars"
    )

    # Metadata
    date_posted = models.DateTimeField(default=timezone.now)
    is_sold = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        help_text="Moderation status of the listing",
    )
    declined_reason = models.TextField(
        blank=True, help_text="Reason for declining the listing"
    )
    viewed_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="viewed_cars",
        blank=True,
        help_text="Users who have viewed this car",
    )

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

    class Meta:
        db_table = "cars_car"
        ordering = ["-date_posted"]
        verbose_name = "Car"
        verbose_name_plural = "Cars"

    def get_main_image(self):
        """Return the first available image"""
        return self.image1 or self.image2 or self.image3
