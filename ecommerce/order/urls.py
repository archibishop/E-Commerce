from . import views
from django.urls import path

urlpatterns = [
    path('order', views.OrderView.as_view(), name='order-products'),
]

app_name = 'order'
