from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Receipt(models.Model):
    retailer = models.CharField(max_length=200)
    purchaseDate = models.DateField(auto_now=False, auto_now_add=False)
    purchaseTime = models.TimeField()
    total = models.DecimalField(max_digits=7, decimal_places=2)
    points = models.IntegerField(default=0)


class Items(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, null=True)       # Establishing a one to many relationship between Receipt and its items
    shortDescription = models.CharField(max_length=200, null=False)
    price = models.DecimalField(max_digits=7, decimal_places=2)