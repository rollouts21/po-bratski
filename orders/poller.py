import os
import django
import requests
import time
import logging
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from .models import Order

logger = logging.getLogger(__name__)
TOKEN = "7931647653:AAFwoeZ_HnZLGFMy4Ncv_giCOrxZKAUvqgA"
ADMIN_CHAT = "820559840"

URL = f"https://api.telegram.org/bot{TOKEN}/"


def process_callback(callback_data, chat_id, message_id):
    try:
        if not callback_data.startswith(("confirm_order_", "reject_order_")):
            return

        parts = callback_data.split("_")
        if len(parts) < 2:
            logger.error("Invalid callback data format")
            return

        # Первый элемент - действие (confirm/reject), последний - ID заказа
        action = parts[0]
        order_id = parts[-1]

        # Проверяем, что действие допустимо
        if action not in ("confirm", "reject"):
            logger.error(f"Unknown action: {action}")
            return

        order = Order.objects.get(id=order_id)
        order.status = "confirmed" if action == "confirm" else "rejected"
        order.save()

        requests.post(
            URL + "sendMessage",
            json={
                "chat_id": chat_id,
                "text": f"✅ Статус заказа #{order_id} изменен на {order.status}",
                "reply_to_message_id": message_id,
            },
        )

        requests.post(
            URL + "editMessageReplyMarkup",
            json={
                "chat_id": chat_id,
                "message_id": message_id,
                "reply_markup": {"inline_keyboard": []},
            },
        )

    except Order.DoesNotExist:
        logger.error(f"order {order_id} not foune")

    except Exception as e:
        logger.error(f"Error processing callback: {e}")


def poll_updates():
    offset = 0
    while True:
        try:
            response = requests.get(
                URL + "getUpdates", params={"offset": offset, "timeout": 30}
            )
            updates = response.json().get("result", [])

            for update in updates:
                if "callback_query" in update:
                    callback = update["callback_query"]
                    process_callback(
                        callback_data=callback["data"],
                        chat_id=callback["message"]["chat"]["id"],
                        message_id=callback["message"]["message_id"],
                    )
                offset = update["update_id"] + 1

            time.sleep(1)

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            time.sleep(5)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            time.sleep(5)


if __name__ == "__main__":
    poll_updates()
