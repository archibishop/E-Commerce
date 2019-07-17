from . import views
from django.urls import path

urlpatterns = [
    path('order', views.OrderView.as_view(), name='order-products'),
    path('history', views.OrderHistoryView.as_view(), name='order-history'),
    path('invoice/<int:id>', views.OrderInvoiceView.as_view(), name='order-invoice'),
    path('pdf/<int:id>', views.GeneratePDFView.as_view(),
         name='order-generate-pdf'),
    path('product/<int:pk>/<int:order_id>', views.OrderProductDetailView.as_view(),
         name='order-product-item'),
]

app_name = 'order'
