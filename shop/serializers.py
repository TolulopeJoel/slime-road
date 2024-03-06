from rest_framework import serializers

from apps.accounts.serializers import CreatorSerializer

from .models import Product


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
