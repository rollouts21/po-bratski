import requests
from django.conf import settings


def send_telegram_message(order_id, order_items, total_price, user):
    message = (
        f"🔔 Новый заказ №{order_id}\n"
        f"Пользователь: {user.get_full_name() or 'Не указано'}\n"
        f"Email: {user.email}\n"
        f"Телефон: {user.phone_number or 'Не указан'}\n"
        f"Итого: {total_price}₽\n\n"
        f"Товары:\n"
    )

    for item in order_items:
        message += f"- {item.product.name} x{item.quantity} — {item.get_cost()}₽\n"

    message += "\nПодтвердить выдачу заказа:\n"
    message += f"/confirm_{order_id}\n"
    message += f"/reject_{order_id}"

    url = f"https://api.telegram.org/bot {settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": settings.TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=data)
