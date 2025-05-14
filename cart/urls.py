from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="detail"),
    path("add/<slug:slug>/", views.add_to_cart, name="add"),
    path("remove/<slug:slug>/", views.remove_from_cart, name="remove"),
    path("update/<slug:slug>/", views.update_cart, name="update"),
    path("status/", views.cart_status, name="cart-status"),
]
