from rest_framework.serializers import ModelSerializer
from .models import Order, OrderService, OrderProduct


class OrderServiceSerializer(ModelSerializer):
    class Meta:
        model = OrderService
        fields = ['id', 'service', 'total', 'mechanic', 'description']

class OrderProductSerializer(ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'amount', 'total', 'discount', 'description']

class OrderPostSerializer(ModelSerializer):
    services = OrderServiceSerializer(many=True, required=False)
    products = OrderProductSerializer(many=True, required=False)

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

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['services'] = OrderServiceSerializer(instance.orderservice_set.all(), many=True).data
    #     representation['products'] = OrderProductSerializer(instance.orderproduct_set.all(), many=True).data
    #     return representation

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

class OrderListSerializer(ModelSerializer):
    services = OrderServiceSerializer(source='orderservice_set', many=True, required=False)
    products = OrderProductSerializer(source='orderproduct_set', many=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'car', 'description', 'total', 'paid', 'landing', 'odo_mileage', 'hev_mileage', 'ev_mileage',
                  'branch', 'manager', 'manager_share', 'created_at', 'services', 'products']
        read_only_fields = ['created_at']


