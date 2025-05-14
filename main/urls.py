from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.popular_list, name="popular_list"),
    path("products", views.product_list, name="product_list"),
    path("product/<slug:slug>", views.product_detail, name="product_detail"),
]
