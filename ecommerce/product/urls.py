from django.urls import path
from . import views

urlpatterns = [
    path('list', views.ProductListView.as_view(), name='product-list'),
]

app_name = 'product'
