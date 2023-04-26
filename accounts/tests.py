from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from orders.models import Order
from shop.models import Product


class TestLoginView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testcreator',
            email='testuser@example.com',
            password='testpass'
        )

    def test_login_returns_token(self):
        url = reverse('login')
        data = {
            'username': 'testcreator',
            'password': 'testpass',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_returns_400_on_invalid_credentials(self):
        url = reverse('login')
        data = {
            'username': 'testcreator',
            'password': 'wrongpass',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
