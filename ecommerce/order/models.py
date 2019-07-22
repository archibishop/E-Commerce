from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.CharField(max_length=1000)
    total = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
