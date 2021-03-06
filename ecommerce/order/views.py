from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from authentication.models import Person
from product.models import Category, Product
from rating.models import Ratings
from .models import Orders
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
import csv
import json
from easy_pdf.views import PDFTemplateView
import stripe
from django.conf import settings
from django.urls import reverse
from django.conf import settings
from notifications.models import Notification
from django.contrib.auth.models import User
from django.utils.translation import gettext
# Create your views here.

class OrderView(View):
    template_name = 'order.html'

    def get(self, request, *args, **kwargs):
        num_notifications = 0
        if self.request.user.is_authenticated:
            num_notifications = get_num_notifications(self.request.user)
        return render(request, self.template_name, {'vendors': get_vendors(), 'categories': get_categories()
                                                    , 'num_notifications': num_notifications})

    def post(self, request, *args, **kwargs):
        quantity_list = request.POST.getlist('quantity')
        items = request.session['selected_items']
        total = 0
        count = 0 
        for item in items:
            item['status_delivered'] = False
            item['quantity'] = quantity_list[count]
            item_total = int(quantity_list[count]) * int(item['price'])
            total = total + item_total
            count = count + 1
        json_items = json.dumps(items)
        order = Orders.objects.create(user=request.user, items=json_items, total=total)
        if 'payment' in request.POST:
            if request.POST['payment'] == 'card':
                return HttpResponseRedirect(reverse('order:order-card', kwargs={'order_id': order.id}))
        message_output = gettext('Order was successfully made')
        messages.info(request, message_output)
        request.session['selected_items'] = []
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class OrderHistoryView(View):
    template_name = 'order_history.html'

    def get(self, request, *args, **kwargs):
        person = Person.objects.get(user=self.request.user)
        orders_list = []
        status_delivered = False
        if person.customer:
            queryset = Orders.objects.filter(
                user__id=self.request.user.id)
            decoder = json.decoder.JSONDecoder()
            for item in queryset:
                new_list = decoder.decode(item.items)
                obj = {
                    'id': item.id,
                    'items': new_list,
                    'total': item.total
                }
                orders_list.append(obj)
        else: 
            queryset = Orders.objects.all()
            decoder = json.decoder.JSONDecoder()
            for item in queryset:
                new_list = decoder.decode(item.items)
                final_list = []
                new_total = 0
                for item_pdt in new_list:
                    product = Product.objects.get(id=item_pdt['id'])
                    if product.user.id == self.request.user.id:
                        final_list.append(item_pdt)
                        new_total =+ (int(item_pdt['price']) * int(item_pdt['quantity']))
                if len(final_list) > 0:
                    obj = {
                        'id': item.id,
                        'items': final_list,
                        'total': new_total
                    }
                    status_delivered = item_pdt['status_delivered']
                    orders_list.append(obj)
        num_notifications = 0
        if self.request.user.is_authenticated:
            num_notifications = get_num_notifications(self.request.user)
        return render(request, self.template_name, {'vendors': get_vendors(),
                 'categories': get_categories(), 'orders_list': orders_list, 
                 'person': person, 'status': status_delivered,
                 'num_notifications': num_notifications})


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
        num_notifications = 0
        if self.request.user.is_authenticated:
            num_notifications = get_num_notifications(self.request.user)
        return render(request, self.template_name, {'vendors': get_vendors(),
                                'categories': get_categories(), 'order':order ,
                                'num_notifications': num_notifications})


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


class OrderProductDetailView(View):
    template_name = 'ordered_product.html'

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(id=kwargs['pk'])
        order = Orders.objects.get(id=kwargs['order_id'])
        person = Person.objects.get(user=self.request.user)
        rating_exists = False
        rating = Ratings.objects.filter(
            user=self.request.user, product=product, order=order)
        if len(rating) > 0:
            rating_exists = True
        num_notifications = 0
        if self.request.user.is_authenticated:
            num_notifications = get_num_notifications(self.request.user)
        return render(request, self.template_name, {'vendors': get_vendors(),
                                                    'categories': get_categories(),
                                                    'product': product,
                                                    'rate': rating_exists,
                                                    'order_id': kwargs['order_id'],
                                                    'person': person,
                                                    'num_notifications': num_notifications})


class OrderRequestCompleteView(View):
    def get(self, request, *args, **kwargs):
        obj = Orders.objects.get(
            id=self.kwargs['id'])
        decoder = json.decoder.JSONDecoder()
        obj_items = decoder.decode(obj.items)
        added_items = "These items ("
        for item in obj_items:
            product = Product.objects.get(id=item['id'])
            if product.user.id == self.request.user.id:
                item['status_delivered'] = True
                added_items = added_items + item['name'] + " ,"
        new_obj_items = json.dumps(obj_items)
        added_items = added_items + ") have been processed by the vendor."
        Orders.objects.filter(id=self.kwargs['id']).update(items=new_obj_items)
        Notification.objects.create(user=obj.user, message=added_items, read=False)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class OrderCsvView(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        writer = csv.writer(response)

        obj = Orders.objects.get(
            id=self.kwargs['id'])
        decoder = json.decoder.JSONDecoder()
        obj_items = decoder.decode(obj.items)
        for item in obj_items:
            csv_list = []
            csv_list.append({'order_id': self.kwargs['id']})
            
            product = Product.objects.get(id=item['id'])
            if product.user.id == self.request.user.id:
                csv_list.append(item)
            writer.writerow(csv_list)
        return response
        
class ChargeView(View):
    def get(self, request, *args, **kwargs):
        order = Orders.objects.get(id=kwargs['order_id'])
        return render(request, 'charge.html', {'key': settings.STRIPE_PUBLISHABLE_KEY
                                               , 'total': order.total, 'id': order.id})

    def post(self, request, *args, **kwargs):
        order = Orders.objects.get(id=kwargs['order_id'])
        stripe.api_key = settings.STRIPE_SECRET_KEY
        charge = stripe.Charge.create(
            amount=order.total,
            currency='usd',
            description='A Django charge',
            source=request.POST['stripeToken']
        )
        message_output = gettext('Order was successfully made')
        messages.info(
            request, message_output)
        request.session['selected_items'] = []
        return HttpResponseRedirect(reverse('product:products-cart'))
        
def get_vendors():
    vendors = Person.objects.filter(customer=False)
    return vendors


def get_categories():
    categories = Category.objects.all()
    return categories


def get_num_notifications(user):
    notifications = Notification.objects.filter(user=user, read=False)
    return len(notifications)
