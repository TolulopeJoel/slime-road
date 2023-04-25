from django.urls import path

from . import views


urlpatterns = [
    path('', views.ProductList.as_view(), name='products_list'),
    path('<str:slug>/', views.ProductDetail.as_view(), name='products_detail'),
]
