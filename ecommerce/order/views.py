from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from authentication.models import Person
from product.models import Category
from .models import Orders
from django.contrib import messages
from django.views.generic.list import ListView
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


class OrderHistoryView(View):
    template_name = 'order_history.html'

    def get(self, request, *args, **kwargs):
        queryset = Orders.objects.filter(
            user__id=self.request.user.id)
        decoder = json.decoder.JSONDecoder()
        orders_list = []
        for item in queryset:
            new_list = decoder.decode(item.items)
            obj = {
                'id': item.id,
                'items': new_list,
                'total': item.total
            }
            orders_list.append(obj)
        return render(request, self.template_name, {'vendors': get_vendors(),
                 'categories': get_categories(), 'orders_list': orders_list})


def get_vendors():
    vendors = Person.objects.filter(customer=False)
    return vendors


def get_categories():
    categories = Category.objects.all()
    return categories
