from rest_framework import serializers
from .models import User, Product, Purchase

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class PurchaseSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    user =  UserSerializer(read_only=True)

    class Meta:
        model = Purchase
        fields = '__all__'
