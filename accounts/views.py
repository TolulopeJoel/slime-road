from rest_framework import generics
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

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
