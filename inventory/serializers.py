from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Product, Service, Car


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'code', 'name', 'amount', 'unit', 'arrival_price', 'sell_price', 'min_amount', 'max_discount',
                  'supplier', 'branch', 'created_at', 'updated_at']
        read_only_fields = ['id', 'branch', 'created_at', 'updated_at']

    def validate(self, data):
        if data.get('sell_price') is not None and data['sell_price'] < data['arrival_price']:
            raise ValidationError("Sell price cannot be lower than the import price.")

        if data.get('max_discount') is not None and (data['max_discount'] < 0 or data['max_discount'] > 100):
            raise ValidationError("Max discount must be between 0 and 100.")

        return data


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
            'id', 'name', 'brand', 'color', 'state_number', 'is_sold',
            'odo_mileage', 'hev_mileage', 'ev_mileage', 'client', 'branch',
            'created_at'
        ]
        read_only_fields = ['id', 'is_sold', 'branch', 'created_at']

