from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('auth/register/', views.RegisterView.as_view(), name='register'),


    path('user/products/', views.CreatorProducts.as_view(), name='user-products'),
    path('user/library/', views.UserLibrary.as_view(), name='user-library'),
]
