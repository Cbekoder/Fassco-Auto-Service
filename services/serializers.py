from decimal import Decimal

from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, DecimalField, PrimaryKeyRelatedField

from branches.serializers import BranchBalanceSerializer
from inventory.models import Product, Car
from inventory.serializers import CarSerializer, ServiceSerializer, ProductSerializer
from users.models import Employee, Client
from users.serializers import ManagerSerializer, ClientSerializer
from .models import Order, OrderService, OrderProduct


class OrderServiceSerializer(ModelSerializer):
    service = ServiceSerializer()
    class Meta:
        model = OrderService
        fields = ['id', 'service', 'total', 'part', 'discount_type', 'discount', 'mechanic', 'description']

    total = DecimalField(max_digits=15, decimal_places=0, required=False)
    discount = DecimalField(max_digits=15, decimal_places=0, required=False)



class OrderProductSerializer(ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'amount', 'total', 'discount_type', 'discount', 'description']

    total = DecimalField(max_digits=15, decimal_places=0, required=False)
    discount = DecimalField(max_digits=15, decimal_places=0, required=False)

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
        fields = ['id', 'client', 'car', 'description', 'overall_total', 'total', 'paid', 'landing', 'odo_mileage', 'hev_mileage', 'ev_mileage',
                  'branch', 'manager', 'start_date', 'end_date', 'plan_date', 'created_at', 'services', 'products']
        read_only_fields = ['id', 'created_at', 'branch', 'overall_total']

    total = DecimalField(max_digits=15, decimal_places=0, required=False)
    landing = DecimalField(max_digits=15, decimal_places=0, required=False)
    manager = PrimaryKeyRelatedField(queryset=Employee.objects.filter(position='manager'), allow_null=True)


    def create(self, validated_data):
        with transaction.atomic():
            services_data = validated_data.pop('services')
            products_data = validated_data.pop('products')

            if products_data and not validated_data['manager']:
                raise ValidationError({'detail': "If product is exist, Manager is required"})

            car = validated_data.get('car')

            if isinstance(car, int):
                car = Car.objects.get(id=car)
            validated_data['total'] =  0
            validated_data['landing'] = 0
            validated_data['overall_total'] = 0

            order = Order.objects.create(**validated_data, branch=car.branch)
            service_responses = []
            product_responses = []
            for service_data in services_data:
                service_i = OrderService.objects.create(order=order, **service_data)
                service_responses.append(service_i)

            for product_data in products_data:
                product_i = OrderProduct.objects.create(order=order, **product_data)
                product_responses.append(product_i)

            order.landing = order.total - order.paid
            order.save()

            order.services = service_responses
            order.products = product_responses
            return order


class OrderListSerializer(ModelSerializer):
    services = OrderServiceSerializer(source='orderservice_set', many=True)
    products = OrderProductSerializer(source='orderproduct_set', many=True)
    total_discount = SerializerMethodField()
    qqs = SerializerMethodField()
    car = CarSerializer()
    manager = ManagerSerializer()
    branch = BranchBalanceSerializer()
    client = ClientSerializer()

    start_date = SerializerMethodField()
    end_date = SerializerMethodField()
    plan_date = SerializerMethodField()
    created_at = SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'client', 'car', 'description', 'overall_total', 'qqs', 'total', 'total_discount', 'paid', 'landing', 'odo_mileage', 'hev_mileage', 'ev_mileage',
                  'branch', 'manager', 'start_date', 'end_date', 'plan_date', 'created_at', 'services', 'products']
        read_only_fields = ['client', 'branch', 'created_at']

    def get_total_discount(self, obj):
        return obj.overall_total - obj.total

    def get_qqs(self, obj):
        return obj.total_discount * Decimal(0.12)

    def get_client(self, obj):
        return Client.objects.get(id=obj.car.client.id)

    def get_start_date(self, obj):
        return obj.start_date.strftime('%d.%m.%Y') if obj.start_date else None

    def get_end_date(self, obj):
        return obj.end_date.strftime('%d.%m.%Y') if obj.end_date else None

    def get_plan_date(self, obj):
        return obj.plan_date.strftime('%d.%m.%Y') if obj.plan_date else None

    def get_created_at(self, obj):
        return obj.created_at.strftime('%d.%m.%Y') if obj.created_at else None
