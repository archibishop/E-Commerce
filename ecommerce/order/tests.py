
from django.test import TestCase, Client
from django.urls import reverse
from .models import Orders
from django.contrib.auth.models import User


# Create your tests here.
class OrdersTestCase(TestCase):
    def test_order_page_displays(self):
        client = Client()
        response = client.get(reverse('order:order-products'))
        self.assertEqual(response.status_code, 200)

    def test_products_page_with_product(self):
        client = Client()
        user = User.objects.create_user(username='user_name',
                                        email='email',
                                        password='password',
                                        first_name='first_name',
                                        last_name='last_name')
        client.login(username='user_name', password='password')
        response = client.get('/product/list')
        response = client.post('/product/cart', {'product_id': 1,
                                                 'product_name': "Airmax shoes",
                                                 'product_price': "9000",
                                                 'product_category': "shoes"},
                               HTTP_REFERER='http://www.google.com')
        session = client.session
        self.assertEqual(len(session['selected_items']), 1)
        response = client.post(reverse('order:order-products'),
                               {'quantity': 2}, HTTP_REFERER='http://www.google.com')
        orders = Orders.objects.all()
        self.assertEqual(len(orders), 1)
        self.assertEqual(response.status_code, 302)
