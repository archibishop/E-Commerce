from django.shortcuts import render
from .models import Product, Category
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from authentication.models import Person
from django.http import HttpResponseRedirect
from django.conf import settings
from notifications.models import Notification
import cloudinary
import os
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext
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
            context['num_notifications'] = get_num_notifications(
                self.request.user)
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
        if self.request.user.is_authenticated:
            person = Person.objects.get(user=self.request.user)
            context['person'] = person
            context['num_notifications'] = get_num_notifications(
                self.request.user)
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
        if self.request.user.is_authenticated:
            person = Person.objects.get(user=self.request.user)
            context['person'] = person
            context['num_notifications'] = get_num_notifications(
                self.request.user)
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
            context['num_notifications'] = get_num_notifications(
                self.request.user)
            context['person'] = person
        context['vendors'] = get_vendors()
        context['categories'] = get_categories()
        return context


class CartView(View):
    template_name = 'cart.html'

    def get(self, request, *args, **kwargs):
        person = ''
        num = 0
        if request.user.is_authenticated:
            person = Person.objects.get(user=self.request.user)
            num = get_num_notifications(self.request.user)
        return render(request, self.template_name, {'vendors': get_vendors()
                             , 'categories': get_categories(), 'person': person
                             ,'num_notifications': num
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
        num_notifications = 0
        if self.request.user.is_authenticated:
            num_notifications = get_num_notifications(self.request.user)
        return render(request, self.template_name, {'vendors': get_vendors()
                                                    , 'categories': get_categories()
                                                    , 'num_notifications': num_notifications})

class ProductCreateView(View):
    template_name = 'add_product.html'
    
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return render(request, self.template_name, {'categories': categories
                                                    ,'title': 'Add Product'})

    def post(self, request, *args, **kwargs):
        myfile = request.FILES['image']
        image_url = cloudinary.uploader.upload(myfile)['url']
        category = Category.objects.get(category_name=request.POST['category'])
        Product.objects.create(
            user=request.user, 
            product_name=request.POST['pdt-name'], 
            description=request.POST['desc'], 
            price=request.POST['price'],
            image=image_url,
            category=category)
        message_output = gettext(
            'You have been successfully created a Product')
        messages.success(request, message_output)
        return render(request, self.template_name, {'categories': get_categories()
                                                    ,'title': 'Add Product'})


class ProductUpdateView(View):
    template_name = 'update_product.html'

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(id=kwargs['id'])
        categories = Category.objects.all()
        return render(request, self.template_name, {'categories': categories
                                                    ,'product': product
                                                    ,'title': 'Update Product'})

    def post(self, request, *args, **kwargs):
        myfile = request.FILES['image']
        image_url = cloudinary.uploader.upload(myfile)['url']
        category = Category.objects.get(category_name=request.POST['category'])
        Product.objects.filter(id=request.POST['pdt-id']).update(
            product_name=request.POST['pdt-name'],
            description=request.POST['desc'],
            price=request.POST['price'],
            image=image_url,
            category=category)
        message_output = gettext(
            'You have been successfully update the Product')
        messages.success(
            request, message_output)
        return HttpResponseRedirect(reverse('product:product-list'))

def get_vendors():
    vendors = Person.objects.filter(customer=False)
    return vendors


def get_categories():
    categories = Category.objects.all()
    return categories


def get_num_notifications(user):
    notifications = Notification.objects.filter(user=user, read=False)
    return len(notifications)
