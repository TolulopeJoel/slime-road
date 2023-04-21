from django.urls import path

from rest_framework.routers import SimpleRouter

from . import views

urlpatterns = [
    path('payouts/', views.PayOut.as_view(), name='payouts-list')
]

router = SimpleRouter()

router.register('orders', views.OrderViewset, basename='orders')

urlpatterns += router.urls
