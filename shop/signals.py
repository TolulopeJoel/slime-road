import cloudinary
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Product


@receiver(pre_delete, sender=Product)
def product_image_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.image.public_id)
