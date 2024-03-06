from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.shop.models import Product
from orders.models import Order


class TestLoginView(APITestCase):
    """
    Test cases for the LoginView API.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testcreator',
            email='testuser@example.com',
            password='testpass'
        )

    def test_login_returns_token(self):
        """
        Test successful user login returns access and refresh tokens.
        """
        url = reverse('login')
        data = {
            'username': 'testcreator',
            'password': 'testpass',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_returns_401_on_invalid_credentials(self):
        """
        Test login returns 401 Unauthorized on invalid credentials.
        """
        url = reverse('login')
        data = {
            'username': 'testcreator',
            'password': 'wrongpass',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestCreatorProducts(APITestCase):
    """
    Test cases for the CreatorProducts API view.
    """

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
        """
        Test API view returns only products created by the authenticated user (creator).
        """
        url = reverse('user-products')
        token = RefreshToken.for_user(self.creator).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Product 2')
        self.assertEqual(response.data[1]['name'], 'Product 1')

    def test_returns_401_if_not_authenticated(self):
        """
        Test API view returns 401 Unauthorized if user is not authenticated.
        """
        url = reverse('user-products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestUserLibrary(APITestCase):
    """
    Test cases for the UserLibrary API view.
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com'
        )
        self.client.force_authenticate(user=self.user)

        self.product1 = Product.objects.create(
            name='Product 1',
            description='Product 1 description',
            price=10.99,
            creator=self.user
        )
        self.product2 = Product.objects.create(
            name='Product 2',
            description='Product 2 description',
            price=5.99,
            creator=self.user
        )

        self.order = Order.objects.create(
            product=self.product1,
            email=self.user.email,
            price=self.product1.price,
            paid=True
        )

    def test_get_user_library(self):
        """
        Test API view returns the library of products bought by the authenticated user.
        """
        url = reverse('user-library')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.product1.name)

    def test_get_user_library_no_orders(self):
        """
        Test API view returns an empty library when the user has no orders.
        """
        self.order.delete()
        url = reverse('user-library')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
