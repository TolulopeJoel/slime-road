from shop.models import Product
from .models import Order


class CreatorPaidOrdersQuerysetMixin:
    """
    Mixin to get a queryset of orders where the product's creator is the requesting user and the order is paid.
    """

    def get_queryset(self):
        user = self.request.user
        orders = Order.objects.filter(paid=True, product__creator=user)
        return orders
