from django.shortcuts import render

from rest_framework import viewsets

from .models import Order
from .serailizers import OrderSerializer


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
