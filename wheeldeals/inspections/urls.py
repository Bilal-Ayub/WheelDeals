from django.urls import path
from . import views

urlpatterns = [
    # Buyer URLs
    path("request/<int:car_id>/", views.request_inspection, name="request_inspection"),
    path("my-requests/", views.buyer_inspection_status, name="buyer_inspection_status"),
    # Seller URLs
    path(
        "seller/requests/",
        views.seller_inspection_requests,
        name="seller_inspection_requests",
    ),
    path(
        "accept/<str:inspection_id>/", views.accept_inspection, name="accept_inspection"
    ),
    path(
        "reject/<str:inspection_id>/", views.reject_inspection, name="reject_inspection"
    ),
    # Inspector URLs
    path("inspector/dashboard/", views.inspector_dashboard, name="inspector_dashboard"),
    path(
        "assign/<str:inspection_id>/", views.assign_inspection, name="assign_inspection"
    ),
    path("start/<str:inspection_id>/", views.start_inspection, name="start_inspection"),
    path(
        "submit-report/<str:inspection_id>/",
        views.submit_inspection_report,
        name="submit_inspection_report",
    ),
    # View report (accessible to buyer, seller, inspector)
    path(
        "report/<str:inspection_id>/",
        views.view_inspection_report,
        name="view_inspection_report",
    ),
]
