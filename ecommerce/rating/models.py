from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from order.models import Orders
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Ratings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='seller')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(
        Orders, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(default=1,
                                 validators=[
                                     MaxValueValidator(5),
                                     MinValueValidator(1)
                                 ])

