from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-input"}),
    )
    full_name = forms.CharField(
        required=True,
        label="ФИО",
        widget=forms.TextInput(attrs={"class": "form-input"}),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-input"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-input"})
    )

    class Meta:
        model = CustomUser
        fields = ("phone_number", "email", "full_name", "password1", "password2")


class CustomLoginForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-input"}),
        label="Номер телефона",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-input"}),
        label="Пароль",
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "city",
            "street",
            "house",
            "apartment",
            "entrance",
            "floor",
        ]
        widgets = {
            "city": forms.TextInput(attrs={"class": "form-input"}),
            "street": forms.TextInput(attrs={"class": "form-input"}),
            "house": forms.TextInput(attrs={"class": "form-input"}),
            "apartment": forms.TextInput(attrs={"class": "form-input"}),
            "entrance": forms.TextInput(attrs={"class": "form-input"}),
            "floor": forms.TextInput(attrs={"class": "form-input"}),
        }
