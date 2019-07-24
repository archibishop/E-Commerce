
from django.test import TestCase, Client
from django.urls import reverse
from .models import Orders
from product.models import Product
from django.contrib.auth.models import User
from authentication.models import Person

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
        Person.objects.create(user=user, customer=True)
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

    def test_order_history_page_displays(self):
        client = Client()
        user = User.objects.create_user(username='user_name',
                                        email='email',
                                        password='password',
                                        first_name='first_name',
                                        last_name='last_name')
        Person.objects.create(user=user, customer=True)                                
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
        response = client.get(reverse('order:order-history'))
        self.assertContains(
            response, 'PDF', status_code=200)

    def test_order_history_seller_page_displays(self):
        client = Client()
        user = User.objects.create_user(username='user_name',
                                        email='email',
                                        password='password',
                                        first_name='first_name',
                                        last_name='last_name')
        Person.objects.create(user=user, customer=True)
        user_seller = User.objects.create_user(username='user_seller',
                                        email='email',
                                        password='password',
                                        first_name='first_name',
                                        last_name='last_name')
        Person.objects.create(user=user_seller, customer=False)
        pdt = Product.objects.create(product_name="Airmax shoes", user=user_seller,
                               price=300, image="image.net.url")
        client.login(username='user_name', password='password')
        response = client.get('/product/list')
        response = client.post('/product/cart', {'product_id': pdt.id,
                                                 'product_name': "Airmax shoes",
                                                 'product_price': "9000",
                                                 'product_category': "shoes"},
                               HTTP_REFERER='http://www.google.com')
        session = client.session
        self.assertEqual(len(session['selected_items']), 1)
        response = client.post(reverse('order:order-products'),
                               {'quantity': 2}, HTTP_REFERER='http://www.google.com')
        client.login(username='user_seller', password='password')
        orders = Orders.objects.all()
        self.assertEqual(len(orders), 1)
        self.assertEqual(response.status_code, 302)
        response = client.get(reverse('order:order-history'))
        self.assertContains(
            response, 'CSV', status_code=200)

    def test_order_history_page_displays_no_orders(self):
        client = Client()
        user = User.objects.create_user(username='user_name',
                                        email='email',
                                        password='password',
                                        first_name='first_name',
                                        last_name='last_name')
        Person.objects.create(user=user, customer=True)
        client.login(username='user_name', password='password')
        response = client.get(reverse('order:order-history'))
        self.assertContains(
            response, 'No Orders', status_code=200)

    def test_order_history_page_seller_displays_no_orders(self):
        client = Client()
        user = User.objects.create_user(username='user_name',
                                        email='email',
                                        password='password',
                                        first_name='first_name',
                                        last_name='last_name')
        Person.objects.create(user=user, customer=False)
        client.login(username='user_name', password='password')
        response = client.get(reverse('order:order-history'))
        self.assertContains(
            response, 'No Orders', status_code=200)

    def test_order_product_page_displays(self):
        client = Client()
        user = User.objects.create_user(username='user_name',
                                        email='email',
                                        password='password',
                                        first_name='first_name',
                                        last_name='last_name')
        Person.objects.create(user=user, customer=True)
        pdt = Product.objects.create(product_name="Airmax shoes", user=user,
                               price=300, image="image.net.url")
        client.login(username='user_name', password='password')
        response = client.get('/product/list')
        response = client.post('/product/cart', {'product_id': pdt.id,
                                                 'product_name': "Airmax shoes",
                                                 'product_price': "9000",
                                                 'product_category': "shoes"},
                               HTTP_REFERER='http://www.google.com')
        response = client.post(reverse('order:order-products'),
                               {'quantity': 2}, HTTP_REFERER='http://www.google.com')
        orders = Orders.objects.all()                      
        response = client.get('/orders/product/' +
                              str(pdt.id) + '/' + str(orders[0].id))
        self.assertContains(
            response, 'Rate Product', status_code=200)
        self.assertEqual(response.status_code, 200)
