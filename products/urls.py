from django.urls import path
from .views import MainPage, CategoryListAPIView, ProductListAPIView, ProductDetailAPIView, PurchaseAPIView

app_name = 'products'

urlpatterns = [
    path('home/', MainPage.as_view(), name='index'),
    path('api/v1/categories/', CategoryListAPIView.as_view(), name='categories'),
    path('api/v1/products/', ProductListAPIView.as_view(), name='products'),
    path('api/v1/products/<slug:slug>/', ProductDetailAPIView.as_view(), name='product'),
    path('api/v1/purchase/', PurchaseAPIView.as_view(), name='purchase'),
]