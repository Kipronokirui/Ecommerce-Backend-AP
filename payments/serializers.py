from rest_framework import routers, serializers, viewsets
from .models import Order, OrderItem
from products.serializers import Product, ProductSerializer
from django.contrib.auth.models import User

class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id', 'username']

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'product']

class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField(read_only=True)
    user = BuyerSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'title', 'total_price', 'order_items', 'user']
    
    def get_order_items(self, obj):
        order_items = obj.order_item.all()
        serializer = OrderItemSerializer(order_items, many=True)
        return serializer.data