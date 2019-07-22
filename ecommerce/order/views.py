from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from authentication.models import Person
from product.models import Category
from .models import Orders
from django.contrib import messages
import json
# Create your views here.

class OrderView(View):
    template_name = 'order.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'vendors': get_vendors(), 'categories': get_categories()})

    def post(self, request, *args, **kwargs):
        quantity_list = request.POST.getlist('quantity')
        items = request.session['selected_items']
        total = 0
        count = 0 
        for item in items:
            item_total = int(quantity_list[count]) * int(item['price'])
            total = total + item_total
            count = count + 1
        json_items = json.dumps(items)
        Orders.objects.create(user=request.user, items=json_items, total=total)
        messages.info(
            request, 'Order was successfully made')
        request.session['selected_items'] = []
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


def get_vendors():
    vendors = Person.objects.filter(customer=False)
    return vendors


def get_categories():
    categories = Category.objects.all()
    return categories
