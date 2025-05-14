# telegram_bot/views.py
import json
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from orders.models import Order
import requests


class TelegramWebhookView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        message = data.get("message")
        callback_query = data.get("callback_query")

        if callback_query:
            self.handle_callback(callback_query)

        return JsonResponse({"status": "ok"})

    def handle_callback(self, callback):
        data = callback["data"]
        order_id = data.split("_")[-1]
        chat_id = callback["message"]["chat"]["id"]

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return

        if data.startswith("confirm_"):
            order.status = "confirmed"
            text = f"✅ Заказ №{order_id} успешно выдан клиенту."
        elif data.startswith("reject_"):
            order.status = "rejected"
            text = f"❌ Заказ №{order_id} отменён."
        else:
            return

        order.save()

        self.send_confirmation(chat_id, text)

    def send_confirmation(self, chat_id, text):
        url = f"https://api.telegram.org/bot {settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": chat_id, "text": text}
        requests.post(url, data=data)
