from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Employee, Supplier, Client


class SupplierSerializer(ModelSerializer):
    full_name = SerializerMethodField()

    class Meta:
        model = Supplier
        fields = ['id', 'first_name', 'last_name', 'full_name', 'debt', 'phone', 'address', 'branch']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name if obj.last_name else ''}"

class SupplierPostSerializer(ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'first_name', 'last_name', 'phone', 'address']



class ManagerSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'full_name', 'phone', 'address', 'commission_per', 'balance']

    def validate(self, data):
        if data.get('commission_per') is None:
            raise ValidationError("Managers must have a commission percentage.")
        return data

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name if obj.last_name else ''}"


class MechanicSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'full_name', 'phone', 'address', 'kpi', 'balance']
        reed_only_fields = ['full_name']

    def validate(self, data):
        if data.get('kpi') is None:
            raise ValidationError("Mechanics must have a KPI.")
        return data

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name if obj.last_name else ''}"

class WorkerSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'full_name', 'phone', 'address', 'salary', 'balance']
        reed_only_fields = ['full_name']

    def validate(self, data):
        if data.get('salary') is None:
            raise ValidationError("Other employees must have a salary.")
        return data

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name if obj.last_name else ''}"


class EmployeeSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'full_name', 'phone', 'balance', 'branch']
        reed_only_fields = ['full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name if obj.last_name else ''}"

class ClientSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'full_name', 'lending', 'phone', 'extra_phone', 'address']
        reed_only_fields = ['full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name if obj.last_name else ''}"


class ClientPostSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'phone', 'extra_phone', 'address']
