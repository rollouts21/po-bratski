from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, Q

from .models import Category, Product


def popular_list(request):
    products = Product.objects.filter(available=True, discount=0)[:3]
    products_disc = Product.objects.filter(discount__gt=0)

    return render(
        request,
        "main/index/index.html",
        {"products": products, "products_disc": products_disc},
    )


def product_list(request, category_slug=None):
    selected_categories = request.GET.getlist("category")
    search_query = request.GET.get("search", "").strip()
    # category = None
    products = Product.objects.filter(available=True)
    categories = (
        Category.objects.annotate(
            num_products=Count("products")  # Закрываем annotate здесь
        )
        .filter(num_products__gt=0)
        .order_by("name")
    )

    filtered_products = Product.objects.all()

    if selected_categories:
        filtered_products = filtered_products.filter(
            category__name__in=selected_categories
        )

    # Фильтр по поиску
    if search_query:
        filtered_products = filtered_products.filter(
            Q(name__iregex=search_query) | Q(description__iregex=search_query)
        )

    grouped_products = []
    for category in categories:
        products = filtered_products.filter(category=category)
        if products.exists():
            grouped_products.append((category, products))

    return render(
        request,
        "main/product/list.html",
        {
            "products": products,
            "category": category,
            "categories": categories,
            "slug_url": category_slug,
            "grouped_products": grouped_products,
            "selected_categories": selected_categories,
            "search_query": search_query,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    extra_images = list(product.images.order_by("position", "id"))
    gallery_images = []

    if product.image:
        try:
            gallery_images.append({"url": product.image.url, "alt": product.name})
        except (ValueError, AttributeError):
            pass

    for image in extra_images:
        try:
            gallery_images.append(
                {"url": image.image.url, "alt": image.alt_text or product.name}
            )
        except (ValueError, AttributeError):
            continue

    if not gallery_images:
        gallery_images = None

    return render(
        request,
        "main/product/detail.html",
        {
            "product": product,
            "gallery_images": gallery_images,
        },
    )
