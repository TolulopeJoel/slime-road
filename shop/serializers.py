from rest_framework import serializers

from .models import Product
from accounts.serializers import CreatorSerializer


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    """
    creator = CreatorSerializer(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'creator',
            'name',
            'description',
            'image',
            'link',
            'slug',
            'price',
        ]
