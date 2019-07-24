from django.test import TestCase, Client
from django.urls import reverse
from product.models import Product
from order.models import Orders
from django.contrib.auth.models import User
from authentication.models import Person
from .models import Notification

# Create your tests here.
class ProductsTestCase(TestCase):
    def test_notification_page_displays(self):
        client = Client()
        user = User.objects.create_user(username='user_name',
                                        email='email',
                                        password='password',
                                        first_name='first_name',
                                        last_name='last_name')
        Person.objects.create(user=user, customer=True)
        client.login(username='user_name', password='password')
        response = client.get('/notifications/items')
        self.assertEqual(response.status_code, 200)

    def test_notification_displays(self):
        client = Client()
        user = User.objects.create_user(username='user_name',
                                        email='email',
                                        password='password',
                                        first_name='first_name',
                                        last_name='last_name')
        Person.objects.create(user=user, customer=True)
        client.login(username='user_name', password='password')
        notif = Notification.objects.create(
            user=user, message="You order has been processed", read=False)
        response = client.get('/notifications/' + str(notif.id))
        self.assertEqual(response.status_code, 200)
