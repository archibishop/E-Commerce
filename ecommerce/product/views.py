from django.shortcuts import render
from .models import Product, Category
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from authentication.models import Person
from django.http import HttpResponseRedirect
from django.conf import settings

# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'

    def get_queryset(self):
        queryset = Product.objects.all()
        if self.request.user.is_authenticated:
            person = Person.objects.get(user=self.request.user)
            if not person.customer:
                queryset = Product.objects.filter(user_id=self.request.user.id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            person = Person.objects.get(user=self.request.user)
            context['person'] = person
        context['vendors'] = get_vendors()
        context['categories'] = get_categories()
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
        context['categories'] = get_categories()
        return context


class ProductsCategoryListView(ListView):
    model = Product
    template_name = 'product_list.html'

    def get_queryset(self):
        queryset = Product.objects.filter(category__category_name=self.kwargs['category_name'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendors'] = get_vendors()
        context['categories'] = get_categories()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            person = Person.objects.get(user=self.request.user)
            context['person'] = person
        context['vendors'] = get_vendors()
        context['categories'] = get_categories()
        return context


class CartView(View):
    template_name = 'cart.html'

    def get(self, request, *args, **kwargs):
        person = Person.objects.get(user=self.request.user)
        return render(request, self.template_name, {'vendors': get_vendors()
                             , 'categories': get_categories(), 'person': person
                            , 'key': settings.STRIPE_PUBLISHABLE_KEY})

    def post(self, request, *args, **kwargs):
        if 'payment' in request.POST:
            HttpResponseRedirect(request.META['HTTP_REFERER'])

        new_item = {
            'id': request.POST['product_id'],
            'name': request.POST['product_name'],
            'price': request.POST['product_price'],
            'category': request.POST['product_category']
        }
        if 'selected_items' in request.session:
            prev_list = request.session['selected_items']
            if new_item not in request.session['selected_items']:
                prev_list.append(new_item)
                request.session['selected_items'] = prev_list
        else:
            request.session['selected_items'] = []
            request.session['selected_items'].append(new_item)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

class CartRemoveItemView(View):
    template_name = 'cart.html'

    def get(self, request, *args, **kwargs):
        prev_list = request.session['selected_items']
        if 'selected_items' in request.session:
            for item in prev_list:
                if item['id'] == str(kwargs['id']):
                    prev_list.remove(item)
        request.session['selected_items'] = prev_list
        return render(request, self.template_name, {'vendors': get_vendors(), 'categories': get_categories()})

def get_vendors():
    vendors = Person.objects.filter(customer=False)
    return vendors


def get_categories():
    categories = Category.objects.all()
    return categories
