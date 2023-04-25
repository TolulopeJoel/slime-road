from shop.models import Product
from .models import Order

class CreatorPaidOrdersQuerysetMixin:
    def get_queryset(self):
        user = self.request.user
        orders = Order.objects.filter(paid=True, product__creator=user)

        return orders
