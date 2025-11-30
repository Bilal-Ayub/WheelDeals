from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.forms import modelformset_factory
from .models import InspectionRequest, InspectionReport, InspectionPhoto
from .forms import (
    AcceptInspectionForm,
    RejectInspectionForm,
    InspectionReportForm,
    InspectionPhotoForm,
)
from cars.models import Car


@login_required
def request_inspection(request, car_id):
    """Buyer requests inspection for a car"""
    car = get_object_or_404(Car, pk=car_id)

    # Check if user is a buyer
    if not request.user.is_buyer():
        messages.error(request, "Only buyers can request inspections.")
        return redirect("car_detail", pk=car_id)

    # Check if buyer can request inspection (30-day rule)
    if not InspectionRequest.can_request_inspection(car, request.user):
        messages.warning(
            request,
            "You have already requested an inspection for this vehicle within the last 30 days. "
            "Please wait before requesting another inspection.",
        )
        return redirect("car_detail", pk=car_id)

    # Create inspection request
    inspection_request = InspectionRequest.objects.create(
        car=car, buyer=request.user, seller=car.seller
    )

    messages.success(
        request,
        f"Inspection request submitted! Your inspection ID is: {inspection_request.inspection_id}",
    )
    return redirect("car_detail", pk=car_id)


@login_required
def seller_inspection_requests(request):
    """Seller views all inspection requests for their cars"""
    if not request.user.is_seller():
        messages.error(request, "Only sellers can access this page.")
        return redirect("home")

    inspection_requests = InspectionRequest.objects.filter(
        seller=request.user
    ).select_related("car", "buyer")

    context = {"requests": inspection_requests}
    return render(request, "inspections/seller_requests.html", context)


@login_required
def accept_inspection(request, inspection_id):
    """Seller accepts inspection and schedules it"""
    inspection = get_object_or_404(
        InspectionRequest, inspection_id=inspection_id, seller=request.user
    )

    if inspection.status != "requested":
        messages.error(request, "This inspection request cannot be accepted.")
        return redirect("seller_inspection_requests")

    if request.method == "POST":
        form = AcceptInspectionForm(request.POST, instance=inspection)
        if form.is_valid():
            inspection = form.save(commit=False)
            inspection.status = "scheduled"
            inspection.save()
            messages.success(
                request,
                f"Inspection {inspection.inspection_id} has been accepted and scheduled!",
            )
            return redirect("seller_inspection_requests")
    else:
        form = AcceptInspectionForm(instance=inspection)

    context = {"form": form, "inspection": inspection}
    return render(request, "inspections/accept_inspection.html", context)


@login_required
def reject_inspection(request, inspection_id):
    """Seller rejects inspection request"""
    inspection = get_object_or_404(
        InspectionRequest, inspection_id=inspection_id, seller=request.user
    )

    if inspection.status != "requested":
        messages.error(request, "This inspection request cannot be rejected.")
        return redirect("seller_inspection_requests")

    if request.method == "POST":
        form = RejectInspectionForm(request.POST, instance=inspection)
        if form.is_valid():
            inspection = form.save(commit=False)
            inspection.status = "rejected"
            inspection.save()
            messages.success(
                request, f"Inspection {inspection.inspection_id} has been rejected."
            )
            return redirect("seller_inspection_requests")
    else:
        form = RejectInspectionForm(instance=inspection)

    context = {"form": form, "inspection": inspection}
    return redirect("car_detail", pk=inspection.car.pk)


@login_required
def inspector_dashboard(request):
    """Inspector views unassigned inspections and can self-assign"""
    if not request.user.is_inspector():
        messages.error(request, "Only inspectors can access this page.")
        return redirect("home")

    # Show all scheduled inspections that are not yet assigned
    unassigned_inspections = InspectionRequest.objects.filter(
        status="scheduled", inspector__isnull=True
    ).select_related("car", "buyer", "seller")

    # Show inspector's own assigned inspections
    assigned_inspections = InspectionRequest.objects.filter(
        inspector=request.user
    ).select_related("car", "buyer", "seller")

    context = {
        "unassigned_inspections": unassigned_inspections,
        "assigned_inspections": assigned_inspections,
    }
    return render(request, "inspections/inspector_dashboard.html", context)


@login_required
def assign_inspection(request, inspection_id):
    """Inspector self-assigns an inspection"""
    if not request.user.is_inspector():
        messages.error(request, "Only inspectors can assign inspections.")
        return redirect("home")

    inspection = get_object_or_404(InspectionRequest, inspection_id=inspection_id)

    if inspection.status != "scheduled":
        messages.error(request, "This inspection is not available for assignment.")
        return redirect("inspector_dashboard")

    if inspection.inspector:
        messages.error(request, "This inspection has already been assigned.")
        return redirect("inspector_dashboard")

    # Assign inspection to current inspector
    inspection.inspector = request.user
    inspection.status = "assigned"
    inspection.save()

    messages.success(
        request, f"You have been assigned to inspection {inspection.inspection_id}!"
    )
    return redirect("inspector_dashboard")


@login_required
def buyer_inspection_status(request):
    """Buyer views their inspection requests and statuses"""
    if not request.user.is_buyer():
        messages.error(request, "Only buyers can access this page.")
        return redirect("home")

    inspections = InspectionRequest.objects.filter(buyer=request.user).select_related(
        "car", "seller", "inspector"
    )

    context = {"requests": inspections}
    return render(request, "inspections/buyer_status.html", context)


@login_required
def start_inspection(request, inspection_id):
    """Inspector marks inspection as in progress"""
    if not request.user.is_inspector():
        messages.error(request, "Only inspectors can access this page.")
        return redirect("home")

    inspection = get_object_or_404(
        InspectionRequest, inspection_id=inspection_id, inspector=request.user
    )

    if inspection.status != "assigned":
        messages.error(request, "This inspection cannot be started.")
        return redirect("inspector_dashboard")

    inspection.status = "in_progress"
    inspection.save()

    messages.success(
        request, f"Inspection {inspection.inspection_id} is now in progress!"
    )
    return redirect("submit_inspection_report", inspection_id=inspection_id)


@login_required
def submit_inspection_report(request, inspection_id):
    """Inspector submits detailed inspection report"""
    if not request.user.is_inspector():
        messages.error(request, "Only inspectors can access this page.")
        return redirect("home")

    inspection = get_object_or_404(
        InspectionRequest, inspection_id=inspection_id, inspector=request.user
    )

    if inspection.status not in ["assigned", "in_progress"]:
        messages.error(request, "This inspection report cannot be submitted.")
        return redirect("inspector_dashboard")

    # Check if report already exists
    try:
        report = inspection.report
        is_new = False
    except InspectionReport.DoesNotExist:
        report = None
        is_new = True

    # Photo formset (allow up to 10 photos)
    PhotoFormSet = modelformset_factory(
        InspectionPhoto, form=InspectionPhotoForm, extra=5, max_num=10, can_delete=False
    )

    if request.method == "POST":
        form = InspectionReportForm(request.POST, instance=report)
        formset = PhotoFormSet(
            request.POST, request.FILES, queryset=InspectionPhoto.objects.none()
        )

        if form.is_valid() and formset.is_valid():
            # Save report
            report = form.save(commit=False)
            report.inspection_request = inspection
            report.save()

            # Save photos
            for photo_form in formset:
                if photo_form.cleaned_data.get("image"):
                    photo = photo_form.save(commit=False)
                    photo.report = report
                    photo.save()

            # Update inspection status to completed
            inspection.status = "completed"
            inspection.save()

            messages.success(
                request,
                f"Inspection report for {inspection.inspection_id} has been submitted successfully!",
            )
            return redirect("inspector_dashboard")
    else:
        form = InspectionReportForm(instance=report)
        formset = PhotoFormSet(queryset=InspectionPhoto.objects.none())

    context = {
        "form": form,
        "formset": formset,
        "inspection": inspection,
        "is_new": is_new,
    }
    return render(request, "inspections/submit_report.html", context)


@login_required
def view_inspection_report(request, inspection_id):
    """View completed inspection report - accessible to buyer, seller, and inspector"""
    inspection = get_object_or_404(InspectionRequest, inspection_id=inspection_id)

    # Check access permissions
    if (
        request.user
        not in [
            inspection.buyer,
            inspection.seller,
            inspection.inspector,
        ]
        and not request.user.is_staff
    ):
        messages.error(request, "You do not have permission to view this report.")
        return redirect("home")

    if inspection.status != "completed":
        messages.error(request, "This inspection report is not yet available.")
        return redirect("home")

    try:
        report = inspection.report
    except InspectionReport.DoesNotExist:
        messages.error(request, "Inspection report not found.")
        return redirect("home")

    context = {"inspection": inspection, "report": report}
    return render(request, "inspections/view_report.html", context)
