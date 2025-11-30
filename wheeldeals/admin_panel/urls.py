from django.urls import path
from . import views

urlpatterns = [
    path("", views.admin_dashboard, name="admin_dashboard"),
    path("pending-ads/", views.pending_ads, name="admin_pending_ads"),
    path("approve-ad/<int:car_id>/", views.approve_ad, name="admin_approve_ad"),
    path("decline-ad/<int:car_id>/", views.decline_ad, name="admin_decline_ad"),
    path("delete-ad/<int:car_id>/", views.delete_ad, name="admin_delete_ad"),
    path("users/", views.user_management, name="admin_user_management"),
    path(
        "users/<int:user_id>/edit-role/",
        views.edit_user_role,
        name="admin_edit_user_role",
    ),
    path("users/<int:user_id>/delete/", views.delete_user, name="admin_delete_user"),
    path("inspections/", views.inspection_oversight, name="admin_inspection_oversight"),
    path(
        "inspections/<str:inspection_id>/reassign/",
        views.reassign_inspector,
        name="admin_reassign_inspector",
    ),
    path("all-listings/", views.all_listings, name="admin_all_listings"),
]
