from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Product, Service, Car


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'code', 'name', 'amount', 'unit', 'arrival_price', 'sell_price', 'min_amount',
                  'supplier', 'branch', 'created_at', 'updated_at']
        read_only_fields = ['id', 'branch', 'created_at', 'updated_at']

    def validate(self, data):
        if data.get('sell_price') is not None and data['sell_price'] < data['arrival_price']:
            raise ValidationError("Sell price cannot be lower than the import price.")

        return data

class ProductPostSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'code', 'name', 'min_amount', 'unit', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductImportDetailSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'code', 'name', 'amount', 'unit', 'arrival_price']

class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'price', 'branch']
        read_only_fields = ['id', 'branch']



class CarSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = [
            'id', 'name', 'brand', 'color', 'state_number', 'vin_code', 'year_manufacture', 'is_sold',
            'odo_mileage', 'hev_mileage', 'ev_mileage', 'client', 'branch',
            'created_at'
        ]
        read_only_fields = ['id', 'branch', 'created_at']

