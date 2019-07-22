from django.test import TestCase, Client
from django.urls import reverse
from .models import Product
from django.contrib.auth.models import User


# Create your tests here.
class ProductsTestCase(TestCase):
    def test_products_page_displays(self):
        client = Client()
        response = client.get('/product/list')
        self.assertEqual(response.status_code, 200)

    def test_products_page_with_product(self):
        client = Client()
        user = User.objects.create_user(username='user_name',
                                        email='email',
                                        password='password',
                                        first_name='first_name',
                                        last_name='last_name')
        Product.objects.create(product_name="Airmax shoes", user=user,
                               price=300, image="image.net.url")
        response = client.get('/product/list')
        self.assertContains(
            response, 'Airmax shoes', status_code=200)
