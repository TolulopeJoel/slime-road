from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
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
