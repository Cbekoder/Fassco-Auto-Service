from rest_framework import serializers
from .models import Order, OrderService, OrderProduct


class OrderServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderService
        fields = ['service', 'total', 'description', 'mechanic']


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product', 'amount', 'total', 'discount', 'description']


class OrderSerializer(serializers.ModelSerializer):
    services = OrderServiceSerializer(many=True)
    products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'car', 'description', 'total', 'paid', 'landing',
            'odo_mileage', 'hev_mileage', 'ev_mileage',
            'branch', 'manager', 'manager_share',
            'created_at', 'services', 'products'
        ]

    def create(self, validated_data):
        services_data = validated_data.pop('services')
        products_data = validated_data.pop('products')

        order = Order.objects.create(**validated_data)

        for service_data in services_data:
            OrderService.objects.create(order=order, **service_data)

        for product_data in products_data:
            OrderProduct.objects.create(order=order, **product_data)

        return order

    def update(self, instance, validated_data):
        services_data = validated_data.pop('services')
        products_data = validated_data.pop('products')

        instance = super().update(instance, validated_data)

        # Update services
        for service_data in services_data:
            service_id = service_data.get('id')
            service_instance = OrderService.objects.get(id=service_id)
            service_instance.total = service_data.get('total', service_instance.total)
            service_instance.save()

        for product_data in products_data:
            product_id = product_data.get('id')
            product_instance = OrderProduct.objects.get(id=product_id)
            product_instance.amount = product_data.get('amount', product_instance.amount)
            product_instance.discount = product_data.get('discount', product_instance.discount)
            product_instance.total = product_data.get('total', product_instance.total)
            product_instance.save()

        return instance
