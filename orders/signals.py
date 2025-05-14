from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .utils import send_telegram_message


@receiver(post_save, sender=Order)
def notify_order_created(sender, instance, created, **kwargs):
    if created:
        order_items = instance.items.all()
        total_price = instance.total_price
        send_telegram_message(instance.id, order_items, total_price, instance.user)
