from decimal import Decimal

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from branches.models import Wallet
from inventory.models import Product
from .models import ExpenseType, Expense, Salary, ImportList, ImportProduct, Debt, BranchFundTransfer, Lending


class BranchFundTransferSerializer(ModelSerializer):
    class Meta:
        model = BranchFundTransfer
        fields = ['id', 'amount', 'description', 'created_at', 'user']

class BranchFundTransferPostSerializer(ModelSerializer):
    class Meta:
        model = BranchFundTransfer
        fields = ['description']


class ImportProductSerializer(ModelSerializer):
    class Meta:
        model = ImportProduct
        fields = ['product_id', 'amount', 'buy_price', 'total_summ']

class ImportListSerializer(ModelSerializer):
    products = ImportProductSerializer(many=True)

    class Meta:
        model = ImportList
        fields = ['total', 'paid', 'debt', 'supplier_id', 'description', 'branch_id', 'products']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        import_list = ImportList.objects.create(**validated_data)

        for product_data in products_data:
            ImportProduct.objects.create(import_list_id=import_list, **product_data)

        if validated_data['debt'] > 0:
            supplier = validated_data['supplier_id']
            supplier.debt += validated_data['debt']  # Assuming supplier has a 'debt' field
            supplier.save()

            for product_data in products_data:
                product = product_data['product_id']
                product.amount += product_data['amount']  # Assuming product has an 'amount' field
                product.save()

        return import_list


class GiveLendingSerializer(ModelSerializer):
    class Meta:
        model = Lending
        fields = ['client_id', 'lending_amount']

    def create(self, validated_data):
        client = validated_data['client_id']
        client.lending += validated_data['lending_amount']
        client.save()
        validated_data['is_lending'] = True
        validated_data['current_lending'] = client.lending
        return Lending.objects.create(**validated_data)


class PayLendingSerializer(ModelSerializer):
    class Meta:
        model = Lending
        fields = ['client_id', 'lending_amount']

    def create(self, validated_data):
        client = validated_data['client_id']
        client.lending -= validated_data['lending_amount']
        client.save()
        validated_data['is_lending'] = False
        validated_data['current_lending'] = client.lending
        return Lending.objects.create(**validated_data)


class LendingListSerializer(ModelSerializer):
    class Meta:
        model = Lending
        fields = ['id', 'client_id', 'lending_amount', 'current_lending', 'created_at']



class ExpenseTypeSerializer(ModelSerializer):
    class Meta:
        model = ExpenseType
        fields = ['id', 'name', 'branch_id']


class ExpenseSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'description', 'type', 'amount', 'from_user_id', 'branch_id', 'created_at']


class SalarySerializer(ModelSerializer):
    class Meta:
        model = Salary
        fields = ['id', 'employee_id', 'description', 'amount', 'from_user_id', 'created_at']


class SalaryPostSerializer(ModelSerializer):
    class Meta:
        model = Salary
        fields = ['id', 'employee_id', 'description', 'amount']

    def create(self, validated_data):
        wallet = Wallet.objects.last()
        employee = validated_data['employee_id']
        position = employee.position
        if position == 'manager':
            pass
        elif position == 'mechanic':
            pass
        elif position == 'other':
            employee.balance -= validated_data['amount']
            wallet.balance -= validated_data['amount']
            wallet.save()
        employee.save()

        return Lending.objects.create(**validated_data)


class DebtSerializer(ModelSerializer):
    class Meta:
        model = Debt
        fields = ['id', 'supplier_id', 'debt_amount', 'is_debt', 'current_debt', 'branch_id', 'created_at']
