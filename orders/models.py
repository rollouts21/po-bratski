from django.db import models
from users.models import CustomUser
from main.models import Product
from django.conf import settings
from django.core.exceptions import ValidationError
from decimal import Decimal


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидание"),
        ("confirmed", "Успешно"),
        ("rejected", "Неуспешно"),
    ]

    DELIVERY_CHOICES = [
        ("pickup", "Самовывоз"),
        ("delivery", "Доставка"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ← Правильный порядок: сначала модель
        on_delete=models.CASCADE,
        related_name="orders",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_CHOICES)
    delivery_date = models.DateField()
    delivery_time = models.TimeField()

    comment = models.TextField(
        blank=True,
        verbose_name="Комментарий",
        help_text="Дополнительная информация для доставки",
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,  # ← Теперь может быть NULL
        blank=True,
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"Заказ №{self.id}"

    def get_total_cost(self):
        """
        Возвращает общую стоимость заказа.
        Если нет OrderItem, возвращает 0.00
        """
        total = sum(item.get_cost() for item in self.items.all())
        return round(total, 2) if total else Decimal("0.00")

    def update_total_price(self):
        """
        Обновляет поле total_price и сохраняет его в БД.
        Используется в админке или других местах, где нужно пересчитать цену.
        """
        self.total_price = self.get_total_cost()
        self.save(update_fields=["total_price"])

    class Meta:
        indexes = [
            models.Index(fields=["user", "-created_at"]),
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_cost(self):
        """
        Возвращает стоимость товара в заказе (цена * количество)
        """
        return round(self.price * self.quantity, 2)
