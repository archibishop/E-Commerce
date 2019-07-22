from . import views
from django.urls import path

urlpatterns = [
    path('order', views.OrderView.as_view(), name='order-products'),
    path('history', views.OrderHistoryView.as_view(), name='order-history'),
]

app_name = 'order'
