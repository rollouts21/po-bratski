# telegram.py
import requests
from django.conf import settings
from .models import Order, OrderItem
import logging

logger = logging.getLogger(__name__)


def send_order_to_telegram(order_id):
    logger.debug("TRYING")
    print("TRY")
    token = "7931647653:AAFwoeZ_HnZLGFMy4Ncv_giCOrxZKAUvqgA"
    chat_id = "820559840"
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        order = Order.objects.get(id=order_id)
        user = order.user  # Получаем связанного пользователя

        # Формируем сообщение
        message = f"📦 <b>Новый заказ #{order.id}</b>\n"
        message += f"👤 <b>Клиент:</b> {user.full_name}\n"
        message += f"📞 <b>Телефон:</b> {user.phone_number}\n"
        message += f"📅 <b>Дата доставки:</b> {order.delivery_date}\n"
        message += f"🕒 <b>Время доставки:</b> {order.delivery_time}\n"
        message += f"🚚 <b>Тип заказа:</b> {dict(Order.DELIVERY_CHOICES)[order.delivery_type]}\n"

        if order.address:
            message += f"📍 <b>Адрес:</b> {order.address}\n"

        message += "\n<b>Состав заказа:</b>\n"
        for item in OrderItem.objects.filter(order=order):
            message += (
                f"• {item.product.name} x {item.quantity} = {item.get_cost()} ₽\n"
            )

        message += f"\n💰 <b>Итого:</b> {order.get_total_cost()} ₽"

        # Inline-кнопка для подтверждения
        reply_markup = {
            "inline_keyboard": [
                [
                    {
                        "text": "✅ Подтвердить выдачу",
                        "callback_data": f"confirm_order_{order_id}",
                    }
                ]
            ]
        }

        data = {
            "chat_id": chat_id,
            "text": message,
            "reply_markup": reply_markup,
            "parse_mode": "HTML",
        }

        logger.info("SUC")
        print("SEC")
        print(data)
        requests.post(url, json=data)
        print("YESYES")
        response = requests.post(url, json=data)

        print(response.status_code)
        print(response.text)
    except Exception as e:
        logger.exception(f"Ошибка отправки в Telegram: {e}")
        print(e)
        print("EROOR")
