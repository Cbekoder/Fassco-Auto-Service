from decimal import Decimal
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from branches.models import Wallet
from .models import ExpenseType, Expense, Salary, ImportList, ImportProduct, Debt, BranchFundTransfer, Lending


class DebtSerializer(ModelSerializer):
    class Meta:
        model = Debt
        fields = ['id', 'supplier', 'debt_amount', 'is_debt', 'current_debt', 'branch', 'created_at']

class GetDebtSerializer(ModelSerializer):
    class Meta:
        model = Debt
        fields = ['id', 'debt_amount', 'is_debt', 'created_at']

class PayDebtSerializer(ModelSerializer):
    class Meta:
        model = Debt
        fields = ['id', 'supplier', 'debt_amount', 'is_debt', 'current_debt', 'branch', 'created_at']


class ImportProductSerializer(ModelSerializer):
    class Meta:
        model = ImportProduct
        fields = ['product', 'amount', 'buy_price', 'total_summ']

class ImportListSerializer(ModelSerializer):
    products = ImportProductSerializer(many=True)

    class Meta:
        model = ImportList
        fields = ['total', 'paid', 'debt', 'supplier', 'description', 'branch', 'products']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        import_list = ImportList.objects.create(**validated_data)
        products_list = []
        for product_data in products_data:
            pro_cr = ImportProduct.objects.create(import_list=import_list, **product_data)
            products_list.append(pro_cr)
        import_list.products = products_list
        return import_list


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



class ExpenseTypeSerializer(ModelSerializer):
    class Meta:
        model = ExpenseType
        fields = ['id', 'name', 'branch']


class ExpenseSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'description', 'type', 'amount', 'from_user', 'branch', 'created_at']


class SalarySerializer(ModelSerializer):
    class Meta:
        model = Salary
        fields = ['id', 'employee', 'description', 'amount', 'from_user', 'created_at']


class SalaryPostSerializer(ModelSerializer):
    class Meta:
        model = Salary
        fields = ['id', 'employee', 'description', 'amount']

    def create(self, validated_data):
        wallet = Wallet.objects.last()
        employee = validated_data['employee']
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
