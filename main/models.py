from django.db import models
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название категории")
    slug = models.SlugField(
        max_length=150, verbose_name="Ссылка для категории (заполняется автоматически)"
    )

    class Meta:
        ordering = [
            "name",
        ]
        indexes = [models.Index(fields=["name"])]
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def get_absolute_url(self):
        return reverse("main:product_list_by_category", args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
        verbose_name="категория",
    )
    name = models.CharField(max_length=150, verbose_name="название товара")
    slug = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name="Ссылка на товар (заполняется автоматически)",
    )

    image = models.ImageField(
        upload_to="products/%Y/%m/%d", blank=True, verbose_name="Изображение"
    )
    description = RichTextField(
        blank=True, verbose_name="Описание букета (не обязательно)"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=0, verbose_name="стоимость"
    )
    available = models.BooleanField(default=True, verbose_name="доступно ли")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    discount = models.DecimalField(
        default=0, max_digits=4, decimal_places=0, verbose_name="скидка в процентах"
    )
    quantity = models.IntegerField(blank=False, verbose_name="количество", default=1)
    purchased = models.IntegerField(
        blank=True, verbose_name="количество продаж", default=0
    )

    class Meta:
        ordering = [
            "name",
        ]
        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["name"]),
            models.Index(fields=["-created"]),
        ]

        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("main:product_detail", args=[self.slug])

    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 0)

        return self.price
