from rest_framework.serializers import ModelSerializer
from .models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserLoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class CustomUserRegisterSerialzier(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

class CustomUserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['address1', 'address2', 'city', 'country', 'province',
                      'postal_code', 'phone']