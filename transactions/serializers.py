from decimal import Decimal

from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, DecimalField
from inventory.serializers import ProductImportDetailSerializer, ProductSerializer
from .models import ExpenseType, Expense, Salary, ImportList, ImportProduct, Debt, BranchFundTransfer, Lending


class DebtSerializer(ModelSerializer):
    class Meta:
        model = Debt
        fields = ['id', 'supplier', 'debt_amount', 'is_debt', 'current_debt', 'branch', 'created_at']

class DebtUpdateSerializer(ModelSerializer):
    class Meta:
        model = Debt
        fields = ['id', 'supplier', 'debt_amount', 'is_debt', 'current_debt', 'branch', 'created_at']
        read_only_fields = ['supplier', 'is_debt', 'current_debt', 'branch', 'created_at']


class GetPayDebtSerializer(ModelSerializer):
    class Meta:
        model = Debt
        fields = ['id', 'supplier', 'debt_amount', 'is_debt', 'current_debt', 'branch', 'created_at']
        read_only_fields = ['is_debt', 'current_debt', 'branch', 'created_at']


class ImportProductSerializer(ModelSerializer):
    total_summ = SerializerMethodField()
    class Meta:
        model = ImportProduct
        fields = ['id', 'product', 'amount', 'buy_price', 'sell_price', 'total_summ']
        read_only_fields = ['total_summ']

    buy_price = DecimalField(max_digits=10, decimal_places=2, required=False)

    def get_total_summ(self, obj):
        return Decimal(obj.amount) * obj.buy_price

class ImportProductGetSerializer(ModelSerializer):
    product = ProductSerializer()
    total_summ = SerializerMethodField()
    class Meta:
        model = ImportProduct
        fields = ['id', 'product', 'amount', 'buy_price', 'sell_price', 'total_summ']

    buy_price = DecimalField(max_digits=10, decimal_places=2, required=False)

    def get_total_summ(self, obj):
        return Decimal(obj.amount) * obj.buy_price

class ImportListSerializer(ModelSerializer):
    products = ImportProductSerializer(many=True)

    class Meta:
        model = ImportList
        fields = ['id', 'total', 'paid', 'debt', 'supplier', 'description', 'created_at', 'branch', 'products']
        read_only_fields = ['total', 'debt', 'created_at', 'branch']

    def create(self, validated_data):
        with transaction.atomic():
            products_data = validated_data.pop('products')
            import_list = ImportList.objects.create(**validated_data, total=0, debt=0)
            products_list = []
            for product_data in products_data:
                pro_cr = ImportProduct.objects.create(import_list=import_list, **product_data)
                products_list.append(pro_cr)

            import_list.debt = import_list.total - import_list.paid
            import_list.save()
            import_list.products = products_list
            return import_list

class GetImportListSerializer(ModelSerializer):
    products = ImportProductGetSerializer(source='importproduct_set', many=True,)

    class Meta:
        model = ImportList
        fields = ['id', 'total', 'paid', 'debt', 'supplier', 'description', 'created_at', 'branch', 'products']


class BranchFundTransferSerializer(ModelSerializer):
    class Meta:
        model = BranchFundTransfer
        fields = ['id', 'amount', 'description', 'created_at', 'user']

class BranchFundTransferPostSerializer(ModelSerializer):
    class Meta:
        model = BranchFundTransfer
        fields = ['description']


class GivePayLendingSerializer(ModelSerializer):
    class Meta:
        model = Lending
        fields = ['client', 'lending_amount']


class LendingListSerializer(ModelSerializer):
    class Meta:
        model = Lending
        fields = ['id', 'client', 'lending_amount', 'current_lending', 'is_lending', 'created_at']

class LendingUpdateSerializer(ModelSerializer):
    class Meta:
        model = Lending
        fields = ['lending_amount']


class ExpenseTypeSerializer(ModelSerializer):
    class Meta:
        model = ExpenseType
        fields = ['id', 'name', 'branch']
        read_only_fields = ['id', 'branch']

class PaymentTypeSerializer(ModelSerializer):
    class Meta:
        model = ExpenseType
        fields = ['id', 'name', 'branch']
        read_only_fields = ['id', 'branch']


class ExpenseSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'description', 'type', 'amount', 'from_user', 'branch', 'created_at']
        read_only_fields = ['id', 'from_user', 'branch', 'created_at']


class SalarySerializer(ModelSerializer):
    class Meta:
        model = Salary
        fields = ['id', 'employee', 'description', 'amount', 'from_user', 'branch', 'created_at']
        read_only_fields = ['id', 'from_user', 'branch', 'created_at']

class SalaryUpdateSerializer(ModelSerializer):
    class Meta:
        model = Salary
        fields = ['id', 'employee', 'description', 'amount', 'from_user', 'branch', 'created_at']
        read_only_fields = ['id', 'employee', 'from_user', 'branch', 'created_at']