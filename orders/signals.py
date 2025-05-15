# # signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Order
# from .telegram import send_order_to_telegram  # Импортируем функцию отправки


# @receiver(post_save, sender=Order)
# def handle_new_order(sender, instance, created, **kwargs):
#     if created:
#         send_order_to_telegram(instance.id)
