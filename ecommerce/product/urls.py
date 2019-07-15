from django.urls import path
from . import views

urlpatterns = [
    path('list', views.ProductListView.as_view(), name='product-list'),
    path('vendor/<int:id>', views.ProductsVendorListView.as_view(),
         name='products-vendor'),
    path('category/<str:category_name>', views.ProductsCategoryListView.as_view(),
         name='products-category'),
]

app_name = 'product'
