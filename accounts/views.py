from rest_framework import generics
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from orders.models import Order
from orders.serailizers import OrderSerializer
from shop.models import Product
from shop.serializers import ProductSerializer


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class CreatorProducts(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(creator=user)


class UserLibrary(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.request.user
        orders = Order.objects.filter(paid=True, email=user.email)
        bought_products = Product.objects.filter(orders__in=orders)
        
        return bought_products
