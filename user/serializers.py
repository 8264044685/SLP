import random
import string

from rest_framework import serializers
from slp_admin.models import *
from slp_admin import models
from .models import Category, Quiz, Question, Video


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:

        model = Question
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    address = []

    class Meta:
        model = SlpUser
        fields = ['email', 'password', 'first_name', 'last_name', 'phone', 'company', 'referred_by']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
            'refer-code': {
                'read_only': True,
            }
        }

    def create(self, validated_data):
        refer_code = ''.join(random.choices(string.ascii_uppercase +
                                            string.digits, k=6))
        slp_user = SlpUser.objects.create(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            company=validated_data['company'],
            refer_code=refer_code,
            referred_by=validated_data['referred_by'],
            address=self.context,
            referred_to=[]
        )
        return slp_user


class QRCodeSerializer(serializers.ModelSerializer):
    """Serializer for QR Code create"""
    product_name = serializers.SerializerMethodField()
    manufacturer_name = serializers.SerializerMethodField()
    product_points = serializers.SerializerMethodField()

    class Meta:
        model = models.ScannedQRCode
        fields = ('QR_code', 'user', 'product', 'product_name', 'manufacturer_name', 'product_points', 'status')
        extra_kwargs = {
            'status': {
                'read_only': True
            },
            'product': {
                'write_only': True
            },
            'QR_code': {
                'write_only': True
            },
            'user': {
                'write_only': True
            },
        }


    def get_product_name(self, obj):
        return obj.product.product_name


    def get_manufacturer_name(self, obj):
        return obj.QR_code.merchant.name


    def get_product_points(self, obj):
        return obj.product.productrewardpoint_set.first().qr_code_scan


class RewardHistorySerializer(serializers.ModelSerializer):
    """Serializer for Reward History List to user"""

    class Meta:
        model = models.PointsTransaction
        fields = ('type', 'point', 'transaction_type', 'updated_at')


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for transaction update and create"""

    class Meta:
        model = models.PointsTransaction
        fields = ('user', 'point', 'transaction_type', 'type', 'splitted')


class DisputeRaiseSerializer(serializers.ModelSerializer):
    """Serializer to raise dispute by user"""

    class Meta:
        model = models.Dispute
        fields = ('user', 'QR_code', 'message')


class ProductActivationSerializer(serializers.ModelSerializer):
    """Serializer for product activation detail fill"""

    class Meta:
        model = models.Product
        fields = ('id', 'a_side_batch', 'a_side_set_temperature', 'b_side_set_temperature', 'hot_set_temperature',
                  'mixing_chamber_size', 'pressure_set', 'starting_drum_temperature')


class GetUserSerializer(serializers.ModelSerializer):
    """Serializer to get data for splitting points to user. """

    class Meta:
        model = models.SlpUser
        fields = ('id', 'first_name', 'last_name', 'email')
