from django.contrib import admin
from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
    ]
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 5
    min_num = 0
    fields = ("image", "alt_text", "position")
    ordering = ("position",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "price",
        "available",
        "created",
        "updated",
        "discount",
        "quantity",
        "purchased",
    ]
    list_filter = [
        "available",
        "created",
        "updated",
    ]
    list_editable = [
        "price",
        "available",
        "discount",
        "quantity",
        "purchased",
    ]
    inlines = [ProductImageInline]

    prepopulated_fields = {"slug": ("name",)}
