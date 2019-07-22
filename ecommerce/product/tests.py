from django.test import TestCase, Client
from django.urls import reverse
from .models import Product, Category
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

    def test_products_page_with_product_vendor(self):
        client = Client()
        user = User.objects.create_user(username='user_name',
                                        email='email',
                                        password='password',
                                        first_name='first_name',
                                        last_name='last_name')
        Product.objects.create(product_name="Airmax shoes", user=user,
                               price=300, image="image.net.url")
        response = client.get('/product/vendor/' + str(user.id))
        self.assertContains(
            response, 'Airmax shoes', status_code=200)

    def test_products_page_with_product_not_vendor(self):
        client = Client()
        response = client.get('/product/vendor/1')
        self.assertNotContains(
            response, 'Airmax shoes', status_code=200)

    def test_products_page_with_product_categroy(self):
        client = Client()
        user = User.objects.create_user(username='user_name',
                                        email='email',
                                        password='password',
                                        first_name='first_name',
                                        last_name='last_name')
        category = Category.objects.create(category_name="shoes")
        Product.objects.create(product_name="Airmax shoes", user=user,
                               price=300, image="image.net.url",
                               category=category)
        response = client.get('/product/category/shoes')
        self.assertContains(
            response, 'Airmax shoes', status_code=200)

    def test_view_product(self):
        client = Client()
        user = User.objects.create_user(username='user_name',
                                        email='email',
                                        password='password',
                                        first_name='first_name',
                                        last_name='last_name')
        product = Product.objects.create(product_name="Airmax shoes", user=user,
                               price=300, image="image.net.url")                    
        response = client.get('/product/' + str(product.id))
        self.assertContains(
            response, 'Airmax shoes', status_code=200)

    def test_add_items_cart(self):
        client = Client()
        response = client.get('/product/list')
        response = client.post('/product/cart', {'product_id': 1,
                                                 'product_name': "Airmax shoes",
                                                 'product_price': "9000",
                                                 'product_category': "shoes"}, HTTP_REFERER='http://www.google.com')
        session = client.session
        self.assertEqual(len(session['selected_items']), 1)
        self.assertEqual(response.status_code, 302)

    def test_add_multiple_items_cart(self):
        client = Client()
        response = client.get('/product/list')
        response = client.post('/product/cart', {'product_id': 2,
                                                 'product_name': "Airmax shoes",
                                                 'product_price': "9000",
                                                 'product_category': "shoes"}, HTTP_REFERER='http://www.google.com')
        response = client.post('/product/cart', {'product_id': 3,
                                                 'product_name': "Airmax shoes",
                                                 'product_price': "9000",
                                                 'product_category': "shoes"}, HTTP_REFERER='http://www.google.com')
        session = client.session
        self.assertEqual(len(session['selected_items']), 2)
        self.assertEqual(response.status_code, 302)

    def test_remove_item_cart(self):
        client = Client()
        response = client.get('/product/list')
        response = client.post('/product/cart', {'product_id': 1,
                                                 'product_name': "Airmax shoes",
                                                 'product_price': "9000",
                                                 'product_category': "shoes"}, HTTP_REFERER='http://www.google.com')
        session = client.session
        self.assertEqual(len(session['selected_items']), 1)
        client.get('/product/cart/remove/1')
        session = client.session
        self.assertEqual(len(session['selected_items']), 0)
        self.assertEqual(response.status_code, 302)
