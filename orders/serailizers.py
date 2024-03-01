from rest_framework import serializers
from .models import Order
from shop.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    """
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        """
        Create a new order based on the validated data.
        """
        product = validated_data['product']
        payment_price = validated_data['price']
        product_price = product.price

        paid = False
        if payment_price == 0.00 and product_price == 0.00:
            paid = True
        elif payment_price >= product_price:
            paid = False
        else:
            raise serializers.ValidationError(
                {'detail': f'You can\'t pay ${payment_price} for a ${product_price} product. Come on.'}
            )

        order = Order(
            product=validated_data['product'],
            email=validated_data['email'],
            price=validated_data['price'],
            paid=paid,
        )
        order.save()

        return order
