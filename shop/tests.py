from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product


class ProductModelTests(APITestCase):
    """
    Test case for the Product model.
    """

    def setUp(self):
        """
        Set up data for the test cases.
        """
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )

        self.product = Product.objects.create(
            creator=self.user,
            name='Test Product',
            description='This is a test product',
            link='https://example.com/test-product',
            slug='test-product',
            price='10.99'
        )

    def test_product_str(self):
        """
        Test the __str__ method of the Product model.
        """
        self.assertEqual(str(self.product), 'Test Product')

    def test_product_ordering(self):
        """
        Test the ordering of products.
        """
        product2 = Product.objects.create(
            creator=self.user,
            name='Second Test Product',
            description='This is another test product',
            link='https://example.com/second-test-product',
            slug='second-test-product',
            price='5.99'
        )
        products = list(Product.objects.all())
        self.assertEqual(products, [product2, self.product])

    def test_product_index_together(self):
        """
        Test the index_together property of the Product model's meta class.
        """
        self.assertEqual(Product._meta.index_together[0], ('id', 'slug'))


class ProductListTests(APITestCase):
    """
    Test case for the ProductList API view.
    """

    def setUp(self):
        """
        Set up data and authenticate the user for the test cases.
        """
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)

    def test_product_list_create(self):
        """
        Test creating a new product via API.
        """
        url = reverse('product-list')
        data = {
            'name': 'New Product',
            'description': 'This is a new product',
            'image': 'https://example.com/image',
            'link': 'https://example.com/new-product',
            'price': '19.99'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'New Product')

    def test_product_list_create_with_existing_name(self):
        """
        Test creating a product with an existing name, which should fail.
        """
        url = reverse('product-list')
        data = {
            'name': 'Test Product',
            'description': 'This is a new product',
            'link': 'https://example.com/new-product',
            'price': '19.99'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_list_retrieve(self):
        """
        Test retrieving a list of products via API.
        """
        url = reverse('product-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        product = Product.objects.create(
            creator=self.user,
            name='Test Product',
            description='This is a test product',
            link='https://example.com/test-product',
            slug='test-product',
            price='10.99'
        )
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Product')

    def test_product_list_update(self):
        """
        Test updating a product via API.
        """
        product = Product.objects.create(
            creator=self.user,
            name='Test Product',
            description='This is a test product',
            image='https://example.com/image',
            link='https://example.com/test-product',
            slug='test-product',
            price='10.99'
        )
        url = reverse('product-detail', kwargs={'slug': product.slug})
        data = {
            'name': 'Updated Product',
            'image': 'https://example.com/images/zebra/',
            'link': 'https://example.com/test-product/renew',
            'description': 'This is an updated product',
            'price': '14.99'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get().name, 'Updated Product')

    def test_product_list_delete(self):
        """
        Test deleting a product via API.
        """
        product = Product.objects.create(
            creator=self.user,
            name='Test Product',
            description='This is a test product',
            link='https://example.com/test-product',
            slug='test-product',
            price='10.99'
        )
        url = reverse('product-detail', kwargs={'slug': product.slug})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)


class ProductDetailTests(APITestCase):
    """
    Test case for the ProductDetail API view.
    """

    def setUp(self):
        """
        Set up data, authenticate the user, and create a test product for the test cases.
        """
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.product = Product.objects.create(
            creator=self.user,
            name='Test Product',
            description='This is a test product',
            link='https://example.com/test-product',
            slug='test-product',
            price='10.99'
        )
        self.client.force_authenticate(user=self.user)

    def test_product_detail_retrieve(self):
        """
        Test retrieving a specific product via API.
        """
        url = reverse('product-detail', kwargs={'slug': self.product.slug})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')

    def test_product_detail_update(self):
        """
        Test updating a specific product via API.
        """
        url = reverse('product-detail', kwargs={'slug': self.product.slug})
        data = {
            'name': 'Updated Product',
            'description': 'This is an updated product',
            'image': 'https://example.com/images/zebra/',
            'link': 'https://example.com/test-product/renew',
            'price': '14.99'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get().name, 'Updated Product')

    def test_product_detail_delete(self):
        """
        Test deleting a specific product via API.
        """
        url = reverse('product-detail', kwargs={'slug': self.product.slug})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
