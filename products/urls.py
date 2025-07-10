from django.urls import path
from .views import MainPage, CategoryListAPIView, ProductListAPIView, ProductDetailAPIView, PurchaseAPIView, CartAPIView, CartItemAPIView

app_name = 'products'

urlpatterns = [
    path('', MainPage.as_view(), name='index'),

    # api
    path('api/v1/categories/', CategoryListAPIView.as_view(), name='categories'),
    path('api/v1/products/', ProductListAPIView.as_view(), name='products'),
    path('api/v1/products/<slug:slug>/', ProductDetailAPIView.as_view(), name='product'),
    path('api/v1/purchase/', PurchaseAPIView.as_view(), name='purchase'),
    path('api/v1/cart/', CartAPIView.as_view(), name='cart'),
    path('api/v1/cart_item/', CartItemAPIView.as_view(), name='cart_item'),
]