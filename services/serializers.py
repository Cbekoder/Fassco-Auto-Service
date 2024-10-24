from django.db import transaction
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, DecimalField

from inventory.models import Product
from users.models import Employee, Client
from .models import Order, OrderService, OrderProduct


class OrderServiceSerializer(ModelSerializer):
    class Meta:
        model = OrderService
        fields = ['id', 'service', 'total', 'part', 'discount', 'mechanic', 'description']

    total = DecimalField(max_digits=15, decimal_places=0, required=False)



class OrderProductSerializer(ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'amount', 'total', 'discount', 'description']

    total = DecimalField(max_digits=15, decimal_places=0, required=False)

    def create(self, validated_data):
        with transaction.atomic():
            total = validated_data['total']
            product = Product.objects.get(id=validated_data['product'])
            calc_total = validated_data['amount'] * product.sell_price * (validated_data['discount'] / 100)
            if total != calc_total:
                validated_data['total'] = calc_total
            order_product = OrderProduct.objects.create(**validated_data)
            return order_product

class OrderPostSerializer(ModelSerializer):
    services = OrderServiceSerializer(many=True, required=False)
    products = OrderProductSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'client', 'car', 'description', 'total', 'paid', 'landing', 'odo_mileage', 'hev_mileage', 'ev_mileage',
                  'branch', 'manager', 'created_at', 'services', 'products']
        read_only_fields = ['id', 'created_at', 'branch']

    total = DecimalField(max_digits=15, decimal_places=0, required=False)
    landing = DecimalField(max_digits=15, decimal_places=0, required=False)


    def create(self, validated_data):
        with transaction.atomic():
            services_data = validated_data.pop('services')
            products_data = validated_data.pop('products')

            manager = validated_data.get('car')

            if isinstance(manager, int):
                manager = Employee.objects.get(id=manager)
            total =  0 if validated_data.get('total') is None else validated_data.get('total')
            landing =  0 if validated_data.get('landing') is None else validated_data.get('landing')
            order = Order.objects.create(**validated_data, branch=manager.branch, total=total, landing=landing)
            total = 0
            service_responses = []
            product_responses = []
            for service_data in services_data:
                service_i = OrderService.objects.create(order=order, **service_data)
                total += service_i.total
                service_responses.append(service_i)

            for product_data in products_data:
                product_i = OrderProduct.objects.create(order=order, **product_data)
                total += product_i.total
                product_responses.append(product_i)

            if order.total != total:
                order.total = total
                order.landing = total - order.paid
                order.save()

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
