from django.utils.text import slugify

from rest_framework import generics
from rest_framework.views import Response, status

from .models import Product
from .serializers import ProductSerializer


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def perform_create(self, serializer):
        name = serializer.validated_data.get('name')
        slug = slugify(name)

        return serializer.save(creator=self.request.user, slug=slug)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'slug'
    serializer_class = ProductSerializer
