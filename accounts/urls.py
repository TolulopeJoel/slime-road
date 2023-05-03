from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('user/products/', views.CreatorProducts.as_view(), name='user-products'),
    path('user/library/', views.UserLibrary.as_view(), name='user-library'),
]
