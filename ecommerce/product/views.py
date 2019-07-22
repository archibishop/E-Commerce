from django.shortcuts import render
from .models import Product
from django.views.generic.list import ListView
from authentication.models import Person

# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendors'] = get_vendors()
        return context


class ProductsVendorListView(ListView):
    model = Product
    template_name = 'product_list.html'

    def get_queryset(self):
        queryset = Product.objects.filter(user_id=self.kwargs['id'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendors'] = get_vendors()
        return context


def get_vendors():
    vendors = Person.objects.filter(customer=False)
    return vendors
