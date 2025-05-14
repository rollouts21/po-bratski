from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from cart.cart import Cart
from .forms import OrderForm
from .models import Order, OrderItem
from main.models import Product
from django.views.decorators.http import require_POST


@login_required
# def checkout(request):
#     cart = Cart(request)

#     if request.method == "POST":
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.user = request.user
#             # order.total_price = cart.get_total_price()
#             order.save()

#             for item in cart:
#                 OrderItem.objects.create(
#                     order=order,
#                     product=item["product"],
#                     quantity=item["quantity"],
#                     price=item["price"],
#                 )

#             cart.clear()
#             return redirect("profile")
#     else:
#         form = OrderForm()

#     return render(
#         request,
#         "checkout.html",
#         {"cart": cart, "form": form, "total_price": cart.get_total_price()},
#     )


def checkout(request):
    cart = Cart(request)

    # Преобразуем cart в сериализуемую структуру
    cart_data = list(cart.__iter__())

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.get_total_price()
            order.save()

            # Создаем OrderItems через slug
            for item in cart_data:
                product = item["product"]  # ← это уже объект Product
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item["quantity"],
                    price=product.price,  # ← обращаемся к атрибуту объекта
                )
            cart.clear()
            return redirect("orders:order_success", order_id=order.id)

    return render(
        request,
        "checkout.html",
        {
            "form": OrderForm(),
            "cart_items": cart_data,
            "total_price": cart.get_total_price(),
        },
    )


@login_required
def order_success(request, order_id):
    # Получаем заказ или возвращаем 404, если не найден или не принадлежит пользователю
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Получаем элементы заказа
    order_items = order.items.all()  # через related_name="items" в OrderItem

    return render(
        request,
        "order.html",
        {
            "order": order,
            "order_items": order_items,
        },
    )
