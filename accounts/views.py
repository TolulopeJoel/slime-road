from rest_framework import generics, permissions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from orders.models import Order
from shop.models import Product
from shop.serializers import ProductSerializer

from .serializers import RegisterUserSerializer


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]


class CreatorProducts(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

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
