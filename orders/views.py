from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, permissions, viewsets
from rest_framework.views import APIView, Response, status

from services.paystack import PayStackSerivce
from shop.models import Product

from .mixins import CreatorPaidOrdersQuerysetMixin
from .models import Order
from .serailizers import OrderSerializer


class OrderViewset(viewsets.ModelViewSet):
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
        except Product.DoesNotExist:
            return Response(
                {'detail': 'This product is not available'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order: Order = serializer.save(product=product)

        if order.price == 0.00:
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        paystack = PayStackSerivce()

        pstack_data = paystack.initialise_payment(
            order.email,
            order.price,
        )

        if pstack_data['status']:
            order.paystack_ref = pstack_data['data']['reference']
            order.save()

            return Response(
                {**serializer.data, **pstack_data['data']},
                status=status.HTTP_201_CREATED
            )

        return Response(
            {'status': False, 'message': 'Couldn\'t process payment, try again'},
            status=status.HTTP_400_BAD_REQUEST
        )


class VerifyOrderPaymentView(APIView):
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        order = get_object_or_404(Order, pk=order_id)

        if order.paid:
            return Response({'message': 'Payment was successful'})

        paystack = PayStackSerivce()
        if paystack.verify_payment(order.paystack_ref):
            order.paid = True
            order.save()

            return Response({'message': 'Payment was successful'})

        return Response({'message': 'Payment failed, try again'})


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
