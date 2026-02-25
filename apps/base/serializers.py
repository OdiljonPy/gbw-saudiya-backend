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
    OrderItem,
)
from django.conf import settings


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ["id", "title", "description", "first_image","second_image","video"]



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","name","price","image","category","rate","is_available","description"]



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","name","image"]

class CategoryDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


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



class OrderItemSerializer(serializers.Serializer):
   product=serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
   quantity=serializers.IntegerField()


class OrderSerializer(serializers.ModelSerializer):
   items = OrderItemSerializer(many=True)


   class Meta:
       model = Order
       fields = ['id', 'full_name', 'email', 'phone_number', 'address', 'description', 'items']
       read_only_fields = ['total_price']

   def create(self, validated_data):
       items_data = validated_data.pop('items')

       total = 0
       for item_data in items_data:
           product = item_data['product']
           quantity = item_data['quantity']
           total += (product.price or 0) * quantity


       order = Order.objects.create(total_price=total, **validated_data)
       for item_data in items_data:
           OrderItem.objects.create(order=order, **item_data)

       return order






