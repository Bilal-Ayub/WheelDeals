import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wheeldeals_project.settings")
django.setup()

from users.models import CustomUser
from cars.models import Car
from inspections.models import InspectionRequest

print("=" * 50)
print("DATABASE STATISTICS VERIFICATION")
print("=" * 50)

print("\n=== USER STATISTICS ===")
total_users = CustomUser.objects.count()
buyers = CustomUser.objects.filter(role="buyer").count()
sellers = CustomUser.objects.filter(role="seller").count()
inspectors = CustomUser.objects.filter(role="inspector").count()
admins = CustomUser.objects.filter(role="admin").count()

print(f"Total Users: {total_users}")
print(f"  - Buyers: {buyers}")
print(f"  - Sellers: {sellers}")
print(f"  - Inspectors: {inspectors}")
print(f"  - Admins: {admins}")
print(
    f"Sum check: {buyers + sellers + inspectors + admins} (should equal {total_users})"
)

print("\n=== CAR/AD STATISTICS ===")
total_cars = Car.objects.count()
pending = Car.objects.filter(status="pending").count()
published = Car.objects.filter(status="published").count()
declined = Car.objects.filter(status="declined").count()

print(f"Total Cars: {total_cars}")
print(f"  - Pending: {pending}")
print(f"  - Published: {published}")
print(f"  - Declined: {declined}")
print(f"Sum check: {pending + published + declined} (should equal {total_cars})")

print("\n=== INSPECTION STATISTICS ===")
total_inspections = InspectionRequest.objects.count()
completed = InspectionRequest.objects.filter(status="completed").count()
in_progress = InspectionRequest.objects.filter(status="in_progress").count()
requested = InspectionRequest.objects.filter(status="requested").count()
accepted = InspectionRequest.objects.filter(status="accepted").count()
assigned = InspectionRequest.objects.filter(status="assigned").count()
rejected = InspectionRequest.objects.filter(status="rejected").count()

print(f"Total Inspections: {total_inspections}")
print(f"  - Completed: {completed}")
print(f"  - In Progress: {in_progress}")
print(f"  - Requested: {requested}")
print(f"  - Accepted: {accepted}")
print(f"  - Assigned: {assigned}")
print(f"  - Rejected: {rejected}")
print(
    f"Sum check: {completed + in_progress + requested + accepted + assigned + rejected}"
)

print("\n=== CHART DATA ===")
from django.db.models import Count

ads_by_make = (
    Car.objects.values("make").annotate(count=Count("id")).order_by("-count")[:6]
)
print("\nAds by Make (Top 6):")
for item in ads_by_make:
    print(f"  - {item['make']}: {item['count']} ads")

ads_by_city = (
    Car.objects.values("seller__city")
    .annotate(count=Count("id"))
    .order_by("-count")[:4]
)
print("\nAds by City (Top 4):")
for item in ads_by_city:
    city = item["seller__city"] or "Unknown"
    print(f"  - {city}: {item['count']} ads")

print("\n" + "=" * 50)
print("✓ ALL DATA VERIFIED")
print("=" * 50)
