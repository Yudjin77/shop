from django.contrib import admin
from .models import Category, Product, Purchase, Cart, CartItem


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Cart) 
admin.site.register(CartItem) 