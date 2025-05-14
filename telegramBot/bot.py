# telegram_bot/bot.py
import os
import django
import sys

# Настройка Django
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop.settings")
django.setup()

# Теперь можно импортировать модели
from orders.models import Order
from django.conf import settings

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CallbackQueryHandler


# --- Обработчики ---
async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    order_id = update.callback_query.data.split("_")[-1]
    try:
        order = Order.objects.get(id=order_id)
        order.status = "confirmed"
        order.save()
        await update.callback_query.edit_message_text(
            text=f"✅ Заказ №{order_id} подтверждён"
        )
    except Order.DoesNotExist:
        await update.callback_query.edit_message_text(text="❌ Заказ не найден")


async def reject_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    order_id = update.callback_query.data.split("_")[-1]
    try:
        order = Order.objects.get(id=order_id)
        order.status = "rejected"
        order.save()
        await update.callback_query.edit_message_text(
            text=f"❌ Заказ №{order_id} отменён"
        )
    except Order.DoesNotExist:
        await update.callback_query.edit_message_text(text="❌ Заказ не найден")


# --- Запуск бота ---
if __name__ == "__main__":
    from telegram.ext import CommandHandler

    application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    confirm_handler = CallbackQueryHandler(confirm_order, pattern="^confirm_")
    reject_handler = CallbackQueryHandler(reject_order, pattern="^reject_")

    application.add_handler(confirm_handler)
    application.add_handler(reject_handler)

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    print("Бот запущен...")
    application.run_polling()
