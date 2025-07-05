from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title

class Product(models.Model):
    name = models.CharField(max_length=256, blank=True, default='')
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    slug = models.SlugField(unique=True, max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Purchase(models.Model):
    username = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchases')
    count_products = models.IntegerField(default=1)

