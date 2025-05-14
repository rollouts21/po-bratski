from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages


from orders.models import Order
from .forms import UserRegisterForm, CustomLoginForm
from .models import CustomUser


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, "users/register.html", {"form": form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main:popular_list")

        else:
            print("Форма невалидна. Ошибки:", form.errors)
        return render(request, "users/register.html", {"form": form})


class LoginView(View):
    def get(self, request):
        form = CustomLoginForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=phone_number, password=password)
            if user is not None:
                login(request, user)
                return redirect("main:popular_list")
        return render(request, "users/login.html", {"form": form})


@login_required
def user_logout(request):
    logout(request)
    return redirect("main:popular_list")  #


class ProfileView(LoginRequiredMixin, generic.DateDetailView):
    model = CustomUser
    template_name = "users/profile.html"
    context_object_name = "user"

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем заказы пользователя и сортируем по дате создания
        context["orders"] = (
            self.object.orders.select_related("user")
            .prefetch_related("items__product")
            .all()
            .order_by("-created_at")
        )
        return context
