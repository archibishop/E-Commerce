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
    path('request/<int:id>', views.OrderRequestCompleteView.as_view(),
         name='order-request'),
    path('csv/<int:id>', views.OrderCsvView.as_view(),
         name='order-csv'),
    path('card/<int:order_id>', views.ChargeView.as_view(), name='order-card'),
]

app_name = 'order'
