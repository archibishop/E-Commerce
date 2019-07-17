from django.test import TestCase, Client
from django.urls import reverse
from .models import Orders
from product.models import Product
from django.contrib.auth.models import User
from django.contrib.messages import get_messages


# Create your tests here.
class RatingsTestCase(TestCase):
    def test_rating_success(self):
        client = Client()
        user = User.objects.create_user(username='user_name',
                                        email='email',
                                        password='password',
                                        first_name='first_name',
                                        last_name='last_name')
        client.login(username='user_name', password='password')
        product = Product.objects.create(product_name="Airmax shoes", user=user,
                                         price=300, image="image.net.url")
        client.login(username='user_name', password='password')
        response = client.get('/product/list')
        response = client.post('/product/cart', {'product_id': 1,
                                                 'product_name': "Airmax shoes",
                                                 'product_price': "9000",
                                                 'product_category': "shoes"},
                               HTTP_REFERER='http://www.google.com')
        response = client.post(reverse('order:order-products'),
                               {'quantity': 2}, HTTP_REFERER='http://www.google.com')
        orders = Orders.objects.all()
        response = client.post('/rate/product', {'product_id': product.id,
                                                 'order_id': orders[0].id,
                                                 'rating': 3,
                                                 'product_category': "shoes"},
                               HTTP_REFERER='http://www.google.com')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[0]),
                         'Order was successfully made')
        self.assertEqual(response.status_code, 302)

    def test_rating_with_no_rating(self):
        client = Client()
        user = User.objects.create_user(username='user_name',
                                        email='email',
                                        password='password',
                                        first_name='first_name',
                                        last_name='last_name')
        client.login(username='user_name', password='password')
        product = Product.objects.create(product_name="Airmax shoes", user=user,
                                         price=300, image="image.net.url")
        client.login(username='user_name', password='password')
        response = client.get('/product/list')
        response = client.post('/product/cart', {'product_id': 1,
                                                 'product_name': "Airmax shoes",
                                                 'product_price': "9000",
                                                 'product_category': "shoes"},
                               HTTP_REFERER='http://www.google.com')
        response = client.post(reverse('order:order-products'),
                               {'quantity': 2}, HTTP_REFERER='http://www.google.com')
        orders = Orders.objects.all()
        response = client.post('/rate/product', {'product_id': 2,
                                                 'order_id': 6,
                                                 'product_category': "shoes"},
                               HTTP_REFERER='http://www.google.com')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]),
                         'You did not select anything for rating')
        self.assertEqual(response.status_code, 302)
