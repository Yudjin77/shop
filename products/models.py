from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=256, blank=True, default='')



class Product(models.Model):
    name = models.CharField(max_length=256, blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    count_products = models.IntegerField(default=1)
