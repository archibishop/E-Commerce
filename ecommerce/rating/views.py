from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from product.models import Product
from order.models import Orders
from django.contrib import messages
from rating.models import Ratings

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
            messages.info(
                request, 'You have successfully rated the product')
        else:
            messages.info(
                request, 'You did not select anything for rating')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
