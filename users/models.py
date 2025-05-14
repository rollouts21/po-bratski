from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(
        self, phone_number, email, full_name, password=None, **extra_fields
    ):
        if not phone_number:
            raise ValueError("Укажите номер телефона")
        if not email:
            raise ValueError("Укажите email")
        if not full_name:
            raise ValueError("Укажите ФИО")

        user = self.model(
            phone_number=phone_number,
            email=self.normalize_email(email),
            full_name=full_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, phone_number, email, full_name, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(
            phone_number, email, full_name, password, **extra_fields
        )


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Номер телефона должен быть в формате: '+79991234567'",
    )
    phone_number = models.CharField(
        "Номер телефона", validators=[phone_regex], max_length=17, unique=True
    )
    email = models.EmailField("Email", unique=True)
    full_name = models.CharField("ФИО", max_length=150)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField("Дата регистрации", default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email", "full_name"]

    def __str__(self):
        return f"{self.full_name} ({self.phone_number})"

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name.split()[0]
