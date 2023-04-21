from datetime import timedelta
from decimal import Decimal

from django.utils import timezone
from rest_framework import generics, viewsets
from rest_framework.views import Response, status

from shop.models import Product

from .models import Order
from .serailizers import OrderSerializer


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        try:
            product_id = request.data.get('product_id')
            product = Product.objects.get(id=product_id)

            serializer = OrderSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            order = serializer.save(product=product)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response(
                {'detail': 'This product is not available'},
                status=status.HTTP_404_NOT_FOUND
            )


class PayOut(generics.ListAPIView):
    queryset = Order.objects.filter(paid=True)
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        payouts = []
        for order in queryset:
            if order.product.creator == user:
                payouts.append(order.id)
                
        return Order.objects.filter(id__in=payouts)
    
    # def get(self, request, *args, **kwargs):
    #     total_earnings = 0
    #     past_30_days = 0
    #     past_7_days = 0
    #     balance = 0
        
    #     paid_orders = super().get_queryset()
        
    #     # calculate total earnings for all orders
    #     for order in paid_orders:
    #         total_earnings += order.price
        
    #     # calculate earnings for past 30 days
    #     paid_orders_30_days = paid_orders.filter(created_at__gte=timezone.now() - timedelta(days=30))
    #     for order in paid_orders_30_days:
    #         past_30_days += order.price
        
    #     # calculate earnings for past 7 days
    #     paid_orders_7_days = paid_orders.filter(created_at__gte=timezone.now() - timedelta(days=7))
    #     for order in paid_orders_7_days:
    #         past_7_days += order.price
        
    #     return Response({
    #         'total_earnings': total_earnings,
    #         'past_30_days_earnings': past_30_days,
    #         'past_7_days_earnings': past_7_days
    #     }, status=status.HTTP_200_OK)

