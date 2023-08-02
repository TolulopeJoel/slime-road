import cloudinary
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Product


@receiver(pre_delete, sender=Product)
def product_image_delete(sender, instance, **kwargs):
    """
    Signal handler to delete the image associated with a Product before it is deleted.
    This uses the Cloudinary API to delete the image from the Cloudinary storage.
    """
    cloudinary.uploader.destroy(instance.image.public_id)
