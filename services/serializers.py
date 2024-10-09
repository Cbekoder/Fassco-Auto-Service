from rest_framework import serializers
from .models import Order, OrderService, OrderProduct

class OrderServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderService
        fields = ['id', 'service', 'total', 'mechanic', 'description']

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'amount', 'total', 'discount', 'description']

class OrderSerializer(serializers.ModelSerializer):
    services = OrderServiceSerializer(many=True)
    products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['car', 'description', 'total', 'paid', 'landing', 'odo_mileage', 'hev_mileage', 'ev_mileage',
                  'branch', 'manager', 'manager_share', 'created_at', 'services', 'products']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        services_data = validated_data.pop('services')
        products_data = validated_data.pop('products')

        order = Order.objects.create(**validated_data)

        service_responses = []
        product_responses = []
        for service_data in services_data:
            service_i = OrderService.objects.create(order=order, **service_data)
            service_responses.append(service_i)

        for product_data in products_data:
            product_i = OrderProduct.objects.create(order=order, **product_data)
            product_responses.append(product_i)
        order.services = service_responses
        order.products = product_responses
        return order

    # def update(self, instance, validated_data):
    #     services_data = validated_data.pop('services')
    #     products_data = validated_data.pop('products')
    #
    #     instance = super().update(instance, validated_data)
    #
    #     instance.orderservice_set.all().delete()
    #     for service_data in services_data:
    #         OrderService.objects.create(order=instance, **service_data)
    #
    #     instance.orderproduct_set.all().delete()
    #     for product_data in products_data:
    #         OrderProduct.objects.create(order=instance, **product_data)
    #
    #     return instance
