from . import views
from django.urls import path

urlpatterns = [
    path('product', views.RateProductView.as_view(),
         name='rate-product'),
]

app_name = 'rate'
