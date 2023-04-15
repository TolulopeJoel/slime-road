from django.utils.text import slugify

from rest_framework import generics
from rest_framework.views import Response, status

from .models import Product
from .serializers import ProductSerializer


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        data = {}

        for key, value in request.data.items():
            data[key] = value

        data['slug'] = slugify(request.data.get('name'))
        data['creator'] = request.user

        product = Product(**data)
        product.save()

        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'slug'
    serializer_class = ProductSerializer
