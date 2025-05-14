from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from main.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID, {})

        # Конвертация старого формата (если есть)
        self.cart = self._migrate_old_format(cart)

    def _migrate_old_format(self, cart_data):
        """Конвертирует старый формат {slug: quantity} в новый"""
        new_cart = {}
        for slug, value in cart_data.items():
            if isinstance(value, int):
                product = Product.objects.filter(slug=slug).first()
                if product:
                    new_cart[slug] = {
                        "quantity": value,
                        "price": str(product.sell_price()),
                    }
            else:
                new_cart[slug] = value
        self.session[settings.CART_SESSION_ID] = new_cart
        return new_cart

    def __iter__(self):
        """Генератор для отображения в шаблонах"""
        product_slugs = self.cart.keys()
        products = Product.objects.filter(slug__in=product_slugs)

        for product in products:
            item = self.cart[str(product.slug)]
            yield {
                "product": product,
                "quantity": item["quantity"],
                "total": float(item["price"]) * item["quantity"],
                "price": float(item["price"]),
            }

    def add(self, product, quantity=1):
        slug = str(product.slug)
        if slug not in self.cart:
            self.cart[slug] = {"quantity": 0, "price": str(product.sell_price())}
        self.cart[slug]["quantity"] += quantity
        self.save()

    def remove(self, slug):
        if slug in self.cart:
            del self.cart[slug]
            self.save()

    def update(self, slug, quantity):
        if slug in self.cart:
            if quantity > 0:
                self.cart[slug]["quantity"] = quantity
            else:
                del self.cart[slug]
            self.save()

    def get_total_price(self):
        return sum(
            float(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def get_total_items(self):
        return sum(item["quantity"] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True


@require_POST
def add_to_cart(request, slug):
    cart = Cart(request)
    product = get_object_or_404(Product, slug=slug)
    cart.add(product)
    return JsonResponse(
        {
            "status": "success",
            "cart_total": cart.get_total_price(),
            "product_qty": cart.cart[str(slug)]["quantity"],
            "total_items": cart.get_total_items(),
        }
    )


def cart_detail(request):
    cart = Cart(request)
    return render(
        request,
        "cart/detail.html",
        {"cart_items": list(cart), "total_price": cart.get_total_price()},
    )


def cart_status(request):
    cart = Cart(request)
    return JsonResponse(
        {"total_items": cart.get_total_items(), "total_price": cart.get_total_price()}
    )


@require_POST
def remove_from_cart(request, slug):
    cart = Cart(request)
    cart.remove(slug)

    # Для AJAX-запросов
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse(
            {
                "status": "success",
                "cart_total": cart.get_total_price(),
                "total_items": cart.get_total_items(),
            }
        )

    return redirect("cart:detail")


@require_POST
def update_cart(request, slug):
    cart = Cart(request)
    try:
        quantity = int(request.POST.get("quantity", 1))
        cart.update(slug, quantity)
    except (ValueError, TypeError):
        pass
    return redirect("cart:detail")
