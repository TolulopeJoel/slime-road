from rest_framework import viewsets
from rest_framework.views import Response, status

from .models import Order
from .serailizers import OrderSerializer

from shop.models import Product


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        try:
            product_id = self.request.data.get('product_id')
            product = Product.objects.get(id=product_id)

            payment_price = serializer.validated_data.get('price')
            product_price = product.price
            paid_payment = False

            if payment_price == 0.00 and product_price == 0.00:
                paid_payment = True
            elif payment_price < product_price:
                return Response(
                    {'detail': f'You can\'t pay {payment_price} for a {product_price} product'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return serializer.save(product=product, price=payment_price, paid=paid_payment)
        except Product.DoesNotExist:
            return Response(
                {'detail': 'This product is not available'},
                status=status.HTTP_404_NOT_FOUND
            )
