from .models import *
from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):

    address = AddressSerializer(required=True)
    class Meta:
        model = SlpUser
        fields = ['email' , 'password' , 'first_name' , 'last_name' , 'phone' , 'company' , 'refer_code' , 'address']
