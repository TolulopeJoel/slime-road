from datetime import timedelta

from django.utils import timezone
from rest_framework import generics, permissions, viewsets
from rest_framework.views import Response, status

from shop.models import Product

from .mixins import CreatorPaidOrdersQuerysetMixin
from .models import Order
from .serailizers import OrderSerializer


class OrderViewset(CreatorPaidOrdersQuerysetMixin, viewsets.ModelViewSet):
    """
    Viewset for managing orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Create a new order for a given product.
        """
        try:
            product_id = request.data.get('product_id')
            product = Product.objects.get(id=product_id)

            serializer = OrderSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(product=product)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response(
                {'detail': 'This product is not available'},
                status=status.HTTP_404_NOT_FOUND
            )


class PayOut(CreatorPaidOrdersQuerysetMixin, generics.ListAPIView):
    """
    API view to get payout information for the creator.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Get the creator's earnings and balance information.
        """
        payouts = self.get_queryset()

        total_earnings = sum(payout.price for payout in payouts)
        # Calculate earnings for past 30 days
        payouts_30_days = payouts.filter(
            updated_at__gte=timezone.now() - timedelta(days=30)
        )

        past_30_days = sum(payout.price for payout in payouts_30_days)
        # Calculate earnings for past 7 days
        payouts_7_days = payouts.filter(
            updated_at__gte=timezone.now() - timedelta(days=7)
        )
        past_7_days = sum(payout.price for payout in payouts_7_days)
        return Response({
            'balance': 0,  # Placeholder for balance calculation
            'total_earnings': total_earnings,
            'past_30_days_earnings': past_30_days,
            'past_7_days_earnings': past_7_days
        }, status=status.HTTP_200_OK)
