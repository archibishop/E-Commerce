from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from authentication.models import Person
from product.models import Category
from .models import Orders
from django.contrib import messages
from django.views.generic.list import ListView
import json
from easy_pdf.views import PDFTemplateView
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
            item['quantity'] = quantity_list[count]
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


class OrderInvoiceView(View):
    template_name = 'order_invoice.html'

    def get(self, request, *args, **kwargs):
        obj = Orders.objects.get(
            id=self.kwargs['id'])
        decoder = json.decoder.JSONDecoder()
        order = {
            'id': obj.id,
            'items': decoder.decode(obj.items),
            'total': obj.total
        }
        return render(request, self.template_name, {'vendors': get_vendors(),
                                'categories': get_categories(), 'order':order })


class GeneratePDFView(PDFTemplateView):
    template_name = 'pdf.html'
    download_filename = 'invoice.pdf'

    def get_context_data(self, **kwargs):
        obj = Orders.objects.get(
            id=self.kwargs['id'])
        decoder = json.decoder.JSONDecoder()
        order = {
            'id': obj.id,
            'items': decoder.decode(obj.items),
            'total': obj.total
        }
        context = super(GeneratePDFView, self).get_context_data(
            pagesize='A4',
            title='Hi there!',
            **kwargs
        )
        context['order'] = order
        context['request'] = self.request
        return context
        
def get_vendors():
    vendors = Person.objects.filter(customer=False)
    return vendors


def get_categories():
    categories = Category.objects.all()
    return categories
