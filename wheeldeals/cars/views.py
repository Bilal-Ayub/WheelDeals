from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Car
from .forms import CarForm, CarSearchForm
from users.utils import create_guest_user, is_guest_user


def home(request):
    """
    Home page view - displays featured/recent cars.

    SQL Query executed by Django ORM:
    SELECT * FROM cars_car
    WHERE is_sold = 0
    ORDER BY date_posted DESC
    LIMIT 4;
    """
    recent_cars = Car.objects.filter(is_sold=False, status="published").order_by(
        "-date_posted"
    )[:4]

    context = {
        "recent_cars": recent_cars,
        "total_cars": Car.objects.filter(is_sold=False, status="published").count(),
    }
    return render(request, "home.html", context)


def car_list(request):
    """
    Car listings page - browse all available cars with search and pagination.

    SQL Queries executed:

    1. Base query (all cars):
    SELECT c.*, u.username
    FROM cars_car c
    JOIN users_customuser u ON c.seller_id = u.id
    WHERE c.is_sold = 0
    ORDER BY c.date_posted DESC;

    2. With search filter:
    SELECT * FROM cars_car
    WHERE (make LIKE '%?%' OR model LIKE '%?%')
      AND is_sold = 0
    ORDER BY date_posted DESC;

    3. With price filter:
    SELECT * FROM cars_car
    WHERE price BETWEEN ? AND ?
      AND is_sold = 0
    ORDER BY date_posted DESC;

    4. Count for pagination:
    SELECT COUNT(*) FROM cars_car WHERE is_sold = 0;
    """
    cars = Car.objects.filter(is_sold=False, status="published").select_related(
        "seller"
    )
    form = CarSearchForm(request.GET)

    # Apply search filters
    if form.is_valid():
        query = form.cleaned_data.get("query")
        min_price = form.cleaned_data.get("min_price")
        max_price = form.cleaned_data.get("max_price")
        transmission = form.cleaned_data.get("transmission")
        fuel_type = form.cleaned_data.get("fuel_type")

        if query:
            cars = cars.filter(
                Q(make__icontains=query)
                | Q(model__icontains=query)
                | Q(description__icontains=query)
            )

        if min_price:
            cars = cars.filter(price__gte=min_price)

        if max_price:
            cars = cars.filter(price__lte=max_price)

        if transmission:
            cars = cars.filter(transmission=transmission)

        if fuel_type:
            cars = cars.filter(fuel_type=fuel_type)

    # Pagination
    paginator = Paginator(cars, 12)  # 12 cars per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "form": form, "total_cars": cars.count()}
    return render(request, "cars/car_list.html", context)


def car_detail(request, pk):
    """
    Car detail page - view specific car with full information.

    SQL Queries executed:

    1. Get car with seller info:
    SELECT c.*, u.username, u.email, u.phone, u.city
    FROM cars_car c
    JOIN users_customuser u ON c.seller_id = u.id
    WHERE c.id = ?;

    2. Update view count (only for unique users):
    UPDATE cars_car
    SET views = views + 1
    WHERE id = ?;

    3. Track unique viewers:
    INSERT INTO cars_car_viewed_by (car_id, customuser_id) VALUES (?, ?);
    """
    car = get_object_or_404(Car.objects.select_related("seller"), pk=pk)

    # Auto-create guest user if not authenticated
    if not request.user.is_authenticated:
        create_guest_user(request)
        messages.info(
            request, "You are browsing as a guest. Contact information will be hidden."
        )

    # Increment views only if user hasn't viewed this car before
    if request.user not in car.viewed_by.all():
        car.viewed_by.add(request.user)
        car.views += 1
        car.save(update_fields=["views"])

    # Check if current user is a guest
    user_is_guest = is_guest_user(request.user)

    # Check if buyer can request inspection (30-day rule)
    can_request_inspection = False
    if (
        request.user.is_authenticated
        and hasattr(request.user, "is_buyer")
        and request.user.is_buyer()
        and request.user != car.seller
    ):
        from inspections.models import InspectionRequest

        can_request_inspection = InspectionRequest.can_request_inspection(
            car, request.user
        )

    # Get completed inspection reports for this car (visible to all users)
    from inspections.models import InspectionRequest

    completed_inspections = (
        InspectionRequest.objects.filter(car=car, status="completed")
        .select_related("inspector", "report")
        .prefetch_related("report__photos")
    )

    context = {
        "car": car,
        "user_is_guest": user_is_guest,
        "can_request_inspection": can_request_inspection,
        "completed_inspections": completed_inspections,
    }
    return render(request, "cars/car_detail.html", context)


@login_required
def car_create(request):
    """
    Add new car listing (Sellers only, not guests or buyers).

    SQL Query executed when form is saved:
    INSERT INTO cars_car (
        make, model, year, price, mileage, color, transmission,
        fuel_type, description, image1, image2, image3,
        seller_id, date_posted, is_sold, views
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, 0, 0);
    """
    # Prevent guest users from creating listings
    if is_guest_user(request.user):
        messages.warning(request, "Please sign up to list your car for sale.")
        return redirect("register")

    # Only sellers can post ads
    if not request.user.is_seller():
        messages.warning(
            request,
            "Only Sellers can post car listings. Your account is registered as a Buyer.",
        )
        return redirect("home")

    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.seller = request.user
            car.status = "pending"  # New listings require admin approval
            car.save()
            messages.success(
                request, "Your car listing has been submitted for admin approval!"
            )
            return redirect("car_detail", pk=car.pk)
    else:
        form = CarForm()

    context = {"form": form, "title": "Add New Car"}
    return render(request, "cars/car_form.html", context)


@login_required
def car_update(request, pk):
    """
    Edit existing car listing (owner only).

    SQL Queries:
    1. Get car: SELECT * FROM cars_car WHERE id = ?;
    2. Update: UPDATE cars_car SET make=?, model=?, year=?, ... WHERE id = ?;
    """
    car = get_object_or_404(Car, pk=pk, seller=request.user)

    if request.method == "POST":
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, "Your car listing has been updated!")
            return redirect("car_detail", pk=car.pk)
    else:
        form = CarForm(instance=car)

    context = {"form": form, "title": "Edit Car", "car": car}
    return render(request, "cars/car_form.html", context)


@login_required
def car_delete(request, pk):
    """
    Delete car listing (owner only).

    SQL Query:
    DELETE FROM cars_car WHERE id = ?;
    """
    car = get_object_or_404(Car, pk=pk, seller=request.user)

    if request.method == "POST":
        car.delete()
        messages.success(request, "Your car listing has been deleted.")
        return redirect("profile")

    context = {"car": car}
    return render(request, "cars/car_confirm_delete.html", context)
