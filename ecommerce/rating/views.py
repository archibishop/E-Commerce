from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from product.models import Product
from order.models import Orders
from django.contrib import messages
from rating.models import Ratings
from django.utils.translation import gettext
# Create your views here.


class RateProductView(View):
    def post(self, request, *args, **kwargs):
        if 'rating' in request.POST and 'product_id' in request.POST:
            id = int(request.POST['product_id'])
            order_id = int(request.POST['order_id'])
            rating = int(request.POST['rating'])
            product = Product.objects.get(id=id)
            order = Orders.objects.get(id=order_id)
            Ratings.objects.create(
                user=request.user, product=product, order=order, rating=int(rating))
            message_output = gettext('You have successfully rated the product')
            messages.info(request, message_output)
        else:
            message_output = gettext('You did not select anything for rating')
            messages.info(request,  message_output)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
