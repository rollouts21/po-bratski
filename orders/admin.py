from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]
    extra = 1  # Количество дополнительных пустых форм для добавления новых OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "created_at",
        "delivery_type",
        "delivery_date",
        "delivery_time",
        "address",
        "total_price",
        "get_total_cost",
    )
    list_filter = ("delivery_type", "delivery_date", "created_at")
    search_fields = ("user__email", "address")
    inlines = [OrderItemInline]
    readonly_fields = ("created_at", "total_price")

    fieldsets = (
        (None, {"fields": ("user", "created_at")}),
        (
            "Доставка",
            {"fields": ("delivery_type", "delivery_date", "delivery_time", "address")},
        ),
        ("Стоимость", {"fields": ("total_price",)}),
    )

    def get_total_cost(self, obj):
        return obj.get_total_cost()

    get_total_cost.short_description = "Общая стоимость (расчётная)"

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.update_total_price()


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price", "get_cost")
    list_filter = ("order", "product")
    search_fields = ("product__name", "order__id")

    def get_cost(self, obj):
        return obj.get_cost()

    get_cost.short_description = "Стоимость"
