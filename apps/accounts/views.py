from rest_framework import generics, permissions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.shop.models import Product
from apps.shop.serializers import ProductSerializer
from apps.orders.models import Order

from .serializers import RegisterUserSerializer


class LoginView(TokenObtainPairView):
    """
    API view for user login using JWT token.
    """
    serializer_class = TokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    """
    API view for user registration.
    """
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]


class CreatorProducts(generics.ListAPIView):
    """
    API view to get a list of products created by the authenticated user (creator).
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Get a queryset of products created by the authenticated user (creator).
        """
        user = self.request.user
        return super().get_queryset().filter(creator=user)


class UserLibrary(generics.ListAPIView):
    """
    API view to get a list of products bought by the authenticated user (in their library).
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Get a queryset of products bought by the authenticated user (in their library).
        """
        user = self.request.user
        orders = Order.objects.filter(paid=True, email=user.email)
        return Product.objects.filter(orders__in=orders)
