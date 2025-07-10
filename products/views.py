from django.shortcuts import render
from django.views import View
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from .serializers import ProductSerializer, PurchaseSerializer, CategorySerializer, CartItemSerializer, CartSerializer
from .models import Category, Product, Purchase, Cart, CartItem
from users.forms import CustomUserLoginForm, CustomUserCreationForm

# Main Page
class MainPage(View):
    def get(self, request):
        data = Category.objects.all()
        context = {
            'categories': data,
            'login_form': CustomUserLoginForm(),
            'register_form': CustomUserCreationForm(),
            }
        return render(request, 'products/index.html', context)


# Categories
class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Products
class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'


# Purchase
class PurchaseAPIView(ListAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer


#Cart
class CartAPIView(RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


#CartItem
class CartItemAPIView(RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer = CartItemSerializer
    