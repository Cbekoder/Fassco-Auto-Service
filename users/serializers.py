from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Employee, Supplier, Client


class SupplierSerializer(ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'first_name', 'last_name', 'debt', 'phone', 'address', 'branch']

class SupplierPostSerializer(ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'first_name', 'last_name', 'phone', 'address']



class ManagerSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'phone', 'address', 'commission_per', 'balance']

    def validate(self, data):
        if data.get('commission_per') is None:
            raise ValidationError("Managers must have a commission percentage.")
        return data

class MechanicSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'phone', 'address', 'kpi', 'balance']

    def validate(self, data):
        if data.get('kpi') is None:
            raise ValidationError("Mechanics must have a KPI.")
        return data

class WorkerSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'phone', 'address', 'salary', 'balance']

    def validate(self, data):
        if data.get('salary') is None:
            raise ValidationError("Other employees must have a salary.")
        return data






class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'lending', 'phone', 'extra_phone', 'address']


class ClientPostSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'phone', 'extra_phone', 'address']
