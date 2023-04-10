from rest_framework import serializers

from .models import Product


class ProductListSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'creator',
            'name',
            'description',
            'slug',
            'price',
            'created_at',
        ]

    def get_description(self, obj):
        """
        Returns the short description of the product
        """
        product_description = (obj.description).split()
        if len(product_description) < 33:
            return ' '.join(product_description)
        return ' '.join(product_description[:33]) + '...'


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'creator',
            'name',
            'description',
            'link',
            'price',
            'created_at',
        ]
