from django.urls import path

from rest_framework.routers import SimpleRouter

from . import views

urlpatterns = [
    path('payouts/', views.PayOut.as_view(), name='payout-list'),
    path('orders/verify/<int:order_id>/', views.VerifyOrderPaymentView.as_view(), name='verify-order-payment'),
]

router = SimpleRouter()

router.register('orders', views.OrderViewset, basename='order')

urlpatterns += router.urls
