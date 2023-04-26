from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from shop.models import Product

from .models import Order


class OrderViewSetTest(APITestCase):
    def setUp(self):
        self.creator = get_user_model().objects.create_user(
            username='testcreator',
            email='creator@example.com',
            password='testpass'
        )
        self.product1 = Product.objects.create(
            name='Product 1',
            creator=self.creator,
            price=10.0,
        )

        self.product2 = Product.objects.create(
            name='Product 2',
            creator=self.creator,
            price=5.99,
        )

        self.order1 = Order.objects.create(
            product=self.product1,
            email='test1@example.com',
            price=10.0,
            paid=True
        )

        self.order2 = Order.objects.create(
            product=self.product2,
            email='test2@example.com',
            price=5.99,
            paid=True
        )

        token = RefreshToken.for_user(self.creator).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_create_order_success(self):
        url = reverse('order-list')
        data = {
            'product_id': self.product1.id,
            'email': 'test@example.com',
            'price': self.product1.price
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 3)

    def test_create_order_with_invalid_product(self):
        url = reverse('order-list')
        data = {
            'product_id': 100, # non-existent product
            'email': 'test@example.com',
            'price': 10.0
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Order.objects.count(), 2)

    def test_retrieve_order_list(self):
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_order_detail(self):
        url = reverse('order-detail', kwargs={'pk': self.order1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test1@example.com')

    def test_update_order(self):
        url = reverse('order-detail', kwargs={'pk': self.order2.pk})
        data = {
            'email': 'test_updated@example.com',
            'price': 25.0,
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test_updated@example.com')
        self.assertEqual(response.data['price'], '25.00')
       
