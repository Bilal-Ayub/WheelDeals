from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .decorators import admin_required
from users.models import CustomUser
from cars.models import Car
from inspections.models import InspectionRequest, InspectionReport


@admin_required
def admin_dashboard(request):
    """
    Main admin dashboard with statistics and overview.
    Shows: total users, breakdown by role, total ads, inspection stats, pending requests.
    """
    # User Statistics
    total_users = CustomUser.objects.count()
    total_buyers = CustomUser.objects.filter(role="buyer").count()
    total_sellers = CustomUser.objects.filter(role="seller").count()
    total_inspectors = CustomUser.objects.filter(role="inspector").count()
    users_online = CustomUser.objects.filter(
        last_login__gte=timezone.now() - timedelta(minutes=30)
    ).count()

    # Car/Ad Statistics
    total_ads = Car.objects.count()
    pending_ads = Car.objects.filter(status="pending").count()
    published_ads = Car.objects.filter(status="published").count()
    declined_ads = Car.objects.filter(status="declined").count()

    # Inspection Statistics
    total_inspections = InspectionRequest.objects.count()
    completed_inspections = InspectionRequest.objects.filter(status="completed").count()
    in_progress_inspections = InspectionRequest.objects.filter(
        status="in_progress"
    ).count()

    # Ads by Make for chart
    ads_by_make = (
        Car.objects.values("make").annotate(count=Count("id")).order_by("-count")[:6]
    )

    # Ads by City for pie chart
    ads_by_city = (
        Car.objects.values("seller__city")
        .annotate(count=Count("id"))
        .order_by("-count")[:4]
    )

    # Get actual pending ads for the pending requests section
    pending_ads_list = (
        Car.objects.filter(status="pending")
        .select_related("seller")
        .order_by("-date_posted")[:5]
    )

    context = {
        "total_users": total_users,
        "total_buyers": total_buyers,
        "total_sellers": total_sellers,
        "total_inspectors": total_inspectors,
        "users_online": users_online,
        "total_ads": total_ads,
        "pending_ads": pending_ads,
        "published_ads": published_ads,
        "declined_ads": declined_ads,
        "total_inspections": total_inspections,
        "completed_inspections": completed_inspections,
        "in_progress_inspections": in_progress_inspections,
        "ads_by_make": ads_by_make,
        "ads_by_city": ads_by_city,
        "pending_ads_list": pending_ads_list,
    }

    return render(request, "admin_panel/dashboard.html", context)


@admin_required
def pending_ads(request):
    """
    Show all pending ads awaiting moderation.
    """
    ads = (
        Car.objects.filter(status="pending")
        .select_related("seller")
        .order_by("-date_posted")
    )

    context = {
        "ads": ads,
    }

    return render(request, "admin_panel/pending_ads.html", context)


@admin_required
def approve_ad(request, car_id):
    """
    Approve a pending ad and publish it.
    """
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        car.status = "published"
        car.save()
        messages.success(request, f"Ad '{car}' has been approved and published.")
        return redirect("admin_pending_ads")

    return redirect("admin_pending_ads")


@admin_required
def decline_ad(request, car_id):
    """
    Decline a pending ad with reason.
    """
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        reason = request.POST.get("reason", "")
        car.status = "declined"
        car.declined_reason = reason
        car.save()
        messages.success(request, f"Ad '{car}' has been declined.")
        return redirect("admin_pending_ads")

    context = {
        "car": car,
    }

    return render(request, "admin_panel/decline_ad.html", context)


@admin_required
def delete_ad(request, car_id):
    """
    Delete any car listing.
    """
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        car_str = str(car)
        car.delete()
        messages.success(request, f"Ad '{car_str}' has been permanently deleted.")
        return redirect("admin_dashboard")

    return redirect("admin_dashboard")


@admin_required
def user_management(request):
    """
    View and manage all users.
    """
    users = CustomUser.objects.all().order_by("-date_joined")

    # Filter by role if specified
    role_filter = request.GET.get("role")
    if role_filter:
        users = users.filter(role=role_filter)

    context = {
        "users": users,
        "role_filter": role_filter,
    }

    return render(request, "admin_panel/user_management.html", context)


@admin_required
def edit_user_role(request, user_id):
    """
    Change a user's role.
    """
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        new_role = request.POST.get("role")
        if new_role in dict(CustomUser.ROLE_CHOICES).keys():
            user.role = new_role
            user.save()
            messages.success(
                request, f"User '{user.username}' role updated to '{new_role}'."
            )
        else:
            messages.error(request, "Invalid role selected.")

        return redirect("admin_user_management")

    context = {
        "user": user,
        "role_choices": CustomUser.ROLE_CHOICES,
    }

    return render(request, "admin_panel/edit_user_role.html", context)


@admin_required
def delete_user(request, user_id):
    """
    Delete a user account.
    """
    user = get_object_or_404(CustomUser, id=user_id)

    # Prevent deleting yourself
    if user.id == request.user.id:
        messages.error(request, "You cannot delete your own account.")
        return redirect("admin_user_management")

    if request.method == "POST":
        username = user.username
        user.delete()
        messages.success(request, f"User '{username}' has been deleted.")
        return redirect("admin_user_management")

    context = {
        "user": user,
    }

    return render(request, "admin_panel/delete_user.html", context)


@admin_required
def inspection_oversight(request):
    """
    View all inspection requests and reports.
    Admin can reassign inspectors and resolve disputes.
    """
    # Get filter parameters
    status_filter = request.GET.get("status", "all")

    inspections = InspectionRequest.objects.select_related(
        "buyer", "car__seller", "inspector"
    ).order_by("-requested_date")

    if status_filter != "all":
        inspections = inspections.filter(status=status_filter)

    context = {
        "inspections": inspections,
        "status_filter": status_filter,
    }

    return render(request, "admin_panel/inspection_oversight.html", context)


@admin_required
def reassign_inspector(request, inspection_id):
    """
    Reassign an inspection to a different inspector.
    """
    inspection = get_object_or_404(InspectionRequest, inspection_id=inspection_id)

    if request.method == "POST":
        inspector_id = request.POST.get("inspector_id")
        if inspector_id:
            inspector = get_object_or_404(CustomUser, id=inspector_id, role="inspector")
            inspection.inspector = inspector
            inspection.status = "assigned"
            inspection.save()
            messages.success(
                request,
                f"Inspection {inspection.inspection_id} reassigned to {inspector.get_full_name() or inspector.username}.",
            )
        else:
            messages.error(request, "Please select an inspector.")

        return redirect("admin_inspection_oversight")

    # Get all inspectors
    inspectors = CustomUser.objects.filter(role="inspector")

    context = {
        "inspection": inspection,
        "inspectors": inspectors,
    }

    return render(request, "admin_panel/reassign_inspector.html", context)


@admin_required
def all_listings(request):
    """
    View all car listings with status.
    """
    status_filter = request.GET.get("status", "all")

    cars = Car.objects.select_related("seller").order_by("-date_posted")

    if status_filter != "all":
        cars = cars.filter(status=status_filter)

    context = {
        "cars": cars,
        "status_filter": status_filter,
    }

    return render(request, "admin_panel/all_listings.html", context)
