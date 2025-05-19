from django.urls import path

from .views import RegisterView, LoginView, ProfileView, user_logout, user_address

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", user_logout, name="logout"),
    path("", ProfileView.as_view(), name="profile"),
    path("edit/", user_address, name="edit_address"),
]
