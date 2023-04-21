from rest_framework import serializers

from .models import Order

from shop.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, many=True)
    
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        product = validated_data['product']
        payment_price = validated_data['price']
        product_price = product.price

        paid = False
        if payment_price == 0.00 and product_price == 0.00:
            paid = True
        elif payment_price >= product_price:
            paid = True
        elif payment_price < product_price:
            raise serializers.ValidationError(
                {'detail': f'You can\'t pay {payment_price} for a {product_price} product'}
            )

        order = Order(product=product, paid=paid, **validated_data)
        order.save()

        return order
