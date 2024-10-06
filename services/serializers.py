from rest_framework import serializers
from .models import Order, OrderService, OrderProduct

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'car_id', 'description', 'total', 'paid', 'landing',
                  'odo_mileage', 'hev_mileage', 'ev_mileage', 'branch_id', 'created_at']


class OrderServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderService
        fields = ['id', 'order_id', 'service_id', 'total', 'description']


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'order_id', 'product_id', 'amount', 'total', 'description']
