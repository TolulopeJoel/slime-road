from django.utils.text import slugify
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer


class ProductList(generics.ListCreateAPIView):
    """
    View to list all products or create a new product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        """
        Create a new product with the given serializer data.
        Automatically generates a slug from the name and sets the creator to the current user.
        """
        name = serializer.validated_data.get('name')
        slug = slugify(name)

        return serializer.save(creator=self.request.user, slug=slug)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update or delete a specific product by its slug.
    """
    queryset = Product.objects.all()
    lookup_field = 'slug'
    serializer_class = ProductSerializer
