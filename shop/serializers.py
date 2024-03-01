from rest_framework import serializers

from .models import Product
from accounts.serializers import CreatorSerializer


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    """
    creator = CreatorSerializer(read_only=True)
    slug = serializers.SlugField(read_only=True)
    image = serializers.SerializerMethodField()

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

    def get_image(self, document):
        request = self.context.get('request')
        file_url = document.image.url
        return request.build_absolute_uri(file_url)
