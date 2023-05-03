from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from environs import Env

from .models import Order

env = Env()
env.read_env()

@receiver(post_save, sender=Order)
def send_product_email(sender, instance, created, **kwargs):
    if instance.paid:
        subject = 'Product Order Confirmation'
        message = f'Thank you for your order. Your {instance.product.name} has been successfully purchased.\n Access it here: {instance.product.link}'
        from_email = env.str('DEFAULT_FROM_EMAIL')
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list)
