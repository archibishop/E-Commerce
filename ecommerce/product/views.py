from django.shortcuts import render
from .models import Product
from django.views.generic.list import ListView

# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
