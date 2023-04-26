from django.urls import path

from rest_framework.routers import SimpleRouter

from . import views

urlpatterns = [
    path('payouts/', views.PayOut.as_view(), name='payout-list')
]

router = SimpleRouter()

router.register('orders', views.OrderViewset, basename='order')

urlpatterns += router.urls
