from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from cart.cart import Cart
from .forms import OrderForm
from .models import Order, OrderItem
from main.models import Product
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import logging

from main.models import Product
from .telegram import send_order_to_telegram

logger = logging.getLogger(__name__)


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
            print("FUNS STAART")
            logger.debug("FUNC STAAAR")
            send_order_to_telegram(order.id)

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


@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)

        # Обработка callback-запроса
        if "callback_query" in data:
            callback_data = data["callback_query"]["data"]
            if callback_data.startswith("confirm_order_"):
                order_id = int(callback_data.split("_")[2])
                try:
                    order = Order.objects.get(id=order_id)
                    order.status = "confirmed"
                    order.save()
                    send_confirmation_message(order_id)
                except Order.DoesNotExist:
                    pass
            if callback_data.startswith("reject_order_"):
                order_id = int(callback_data.split("_")[2])
                try:
                    order = Order.objects.get(id=order_id)
                    order.status = "rejected"
                    order.save()
                    send_confirmation_message(order_id)
                except Order.DoesNotExist:
                    pass

        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "invalid request"}, status=400)


def send_success_message(order_id):
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        order = Order.objects.get(id=order_id)
        user = order.user

        message = f"✅ <b>Заказ #{order_id} подтвержден</b>\n"
        message += f"👤 Клиент: {user.full_name}\n"
        message += f"💰 Итоговая сумма: {order.total_price} ₽"

        data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}

        requests.post(url, json=data)
    except Exception as e:
        print(f"Ошибка отправки уведомления о подтверждении: {e}")


def send_reject_message(order_id):
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        order = Order.objects.get(id=order_id)
        user = order.user
        message = f"✅ <b>Заказ #{order_id} отменен</b>\n"
        message += f"👤 Клиент: {user.full_name}\n"
        message += f"💰 Итоговая сумма: {order.total_price} ₽"

        data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}

        requests.post(url, json=data)
    except Exception as e:
        print(f"Ошибка отправки уведомления о подтверждении: {e}")
