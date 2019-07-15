from django.urls import path
from . import views

urlpatterns = [
    path('list', views.ProductListView.as_view(), name='product-list'),
    path('vendor/<int:id>', views.ProductsVendorListView.as_view(),
         name='products-vendor'),
]

app_name = 'product'
