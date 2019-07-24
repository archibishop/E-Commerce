from django.urls import path
from . import views

urlpatterns = [
     path('list', views.ProductListView.as_view(), name='product-list'),
     path('vendor/<int:id>', views.ProductsVendorListView.as_view(),
          name='products-vendor'),
     path('category/<str:category_name>', views.ProductsCategoryListView.as_view(),
          name='products-category'),
     path('<int:pk>', views.ProductDetailView.as_view(),
          name='product-item'),
     path('cart', views.CartView.as_view(), name='products-cart'),
     path('cart/remove/<int:id>', views.CartRemoveItemView.as_view(),
          name='product-cart-remove'),
     path('create', views.ProductCreateView.as_view(),
          name='product-create'),
     path('update/<int:id>', views.ProductUpdateView.as_view(),
         name='product-update'),
]

app_name = 'product'
