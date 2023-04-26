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


class TestCreatorProducts(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.creator = get_user_model().objects.create_user(
            username='testcreator',
            email='creator@example.com',
            password='testpass'
        )
        self.other_creator = get_user_model().objects.create_user(
            username='othertestcreator',
            email='othercreator@example.com',
            password='othertestpass'
        )
        self.product1 = Product.objects.create(
            name='Product 1',
            creator=self.creator,
            price=10.0,
        )
        self.product2 = Product.objects.create(
            name='Product 2',
            creator=self.creator,
            price=20.0,
        )
        self.other_product = Product.objects.create(
            name='Other Product',
            creator=self.other_creator,
            price=30.0,
        )

    def test_returns_only_creator_products(self):
        url = reverse('user-products')
        token = RefreshToken.for_user(self.creator).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Product 2')
        self.assertEqual(response.data[1]['name'], 'Product 1')

    def test_returns_401_if_not_authenticated(self):
        url = reverse('user-products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)




