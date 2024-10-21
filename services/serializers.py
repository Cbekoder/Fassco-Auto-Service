from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from users.models import Employee, Client
from .models import Order, OrderService, OrderProduct


class OrderServiceSerializer(ModelSerializer):
    class Meta:
        model = OrderService
        fields = ['id', 'service', 'total', 'part', 'discount', 'mechanic', 'description']


class OrderProductSerializer(ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'amount', 'total', 'discount', 'description']

class OrderPostSerializer(ModelSerializer):
    services = OrderServiceSerializer(many=True, required=False)
    products = OrderProductSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'client', 'car', 'description', 'total', 'paid', 'landing', 'odo_mileage', 'hev_mileage', 'ev_mileage',
                  'branch', 'manager', 'created_at', 'services', 'products']
        read_only_fields = ['id', 'created_at', 'branch']


    def create(self, validated_data):
        services_data = validated_data.pop('services')
        products_data = validated_data.pop('products')

        manager = validated_data.get('car')

        if isinstance(manager, int):
            manager = Employee.objects.get(id=manager)

        order = Order.objects.create(**validated_data, branch=manager.branch)

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


class OrderListSerializer(ModelSerializer):
    services = OrderServiceSerializer(source='orderservice_set', many=True)
    products = OrderProductSerializer(source='orderproduct_set', many=True)

    class Meta:
        model = Order
        fields = ['id', 'client', 'car', 'description', 'total', 'paid', 'landing', 'odo_mileage', 'hev_mileage', 'ev_mileage',
                  'branch', 'manager', 'created_at', 'services', 'products']
        read_only_fields = ['client', 'branch', 'created_at']

    def get_client(self, obj):
        return Client.objects.get(id=obj.car.client.id)
