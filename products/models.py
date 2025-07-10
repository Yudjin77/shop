import uuid
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(max_length=256, blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveBigIntegerField(default=1)
    slug = models.SlugField(unique=True, max_length=256, blank=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')


class Cart(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    total_price = models.PositiveIntegerField()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart')
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Purchase(models.Model):
    username = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    delivery_address = models.CharField(max_length=256)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchases')


