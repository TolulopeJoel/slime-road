from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),

    path('user/products/', views.CreatorProducts.as_view(), name='user-products'),
]
