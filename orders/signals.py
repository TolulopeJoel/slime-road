from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order

@receiver(post_save, sender=Order)
def send_product_email(sender, instance, created, **kwargs):
    if instance.paid:
        subject = 'Product Order Confirmation'
        message = f'Thank you for your order. Your {instance.product.name} has been successfully purchased.\n Acces it here {instance.product.link}'
        from_email = 'your@email.com'
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list)
