from rest_framework import serializers
from .models import (
    Banner,
    Sponsorship,
    Message,
    Product,
    Category,
    AboutUs,
    Statistics,
    Order,
)
from django.conf import settings


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ["id", "title", "description", "first_image","second_image","video"]



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","name","price","image","category","rate","is_available"]



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","name","image"]



class SponsorshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsorship
        fields = ["id","image"]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id","full_name","email","message","phone_number"]


class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = ["id","name","number"]



class AboutUsSerializer(serializers.ModelSerializer):
    statistics = StatisticsSerializer(many=True,read_only=True)
    class Meta:
        model = AboutUs
        fields = ["id","name","subtitle","statistics","description","image","employer_image"]




class OrderSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta:
        model = Order
        fields = ["id","full_name","email","phone_number","address","description","product_id"]

