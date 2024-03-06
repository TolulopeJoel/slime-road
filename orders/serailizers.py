from rest_framework import serializers
from rest_framework.exceptions import NotFound

from shop.serializers import ProductSerializer

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    """
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Order
        read_only_fields = ['paystack_ref']
        fields = '__all__'

    def create(self, validated_data):
        """
        Create a new order based on the validated data.
        """
        product = validated_data.get('product')

        if not product:
            return NotFound('Product not found')

        payment_price = validated_data.get('price', 0)
        product_price = product.price
        is_paid = False

        if payment_price == 0.00 and product_price == 0.00:
            is_paid = True
        elif payment_price < product_price:
            raise serializers.ValidationError({
                "detail": f" You can't pay ${payment_price} for a ${product_price} product. Come on!"
            })

        return Order.objects.create(
            product=validated_data['product'],
            email=validated_data['email'],
            price=payment_price,
            paid=is_paid,
        )
