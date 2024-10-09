from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from branches.models import Wallet
from users.permissions import IsStaffStatus
from .models import ExpenseType, Expense, Salary, ImportList, ImportProduct, Debt, BranchFundTransfer, Lending
from .serializers import (
    ExpenseTypeSerializer, ExpenseSerializer, SalarySerializer,
    ImportListSerializer, ImportProductSerializer, DebtSerializer,
    BranchFundTransferSerializer, BranchFundTransferPostSerializer, LendingListSerializer,
    SalaryPostSerializer, GetDebtSerializer, PayDebtSerializer, GivePayLendingSerializer
)


class GetDebtCreateView(CreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = GetDebtSerializer
    permission_classes = (IsAuthenticated,)
    
    def perform_create(self, serializer):
        branch = self.request.user.branch
        serializer.save(
            branch=branch,
            is_debt=True,
        )

class PayDebtCreateView(CreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = PayDebtSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        branch = self.request.user.branch
        serializer.save(
            branch=branch,
            is_debt=False,
        )

class DebtListView(ListAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(branch=self.request.user.branch)

class DebtDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
    permission_classes = [IsAuthenticated]


class ImportListCreateView(APIView):
    @transaction.atomic
    def post(self, request):
        import_list_data = {
            'total': request.data.get('total'),
            'paid': request.data.get('paid'),
            'debt': request.data.get('debt'),
            'supplier': request.data.get('supplier'),
            'description': request.data.get('description'),
            'branch': request.user.branch,
        }

        import_list_serializer = ImportListSerializer(data=import_list_data)

        if import_list_serializer.is_valid():
            import_list = import_list_serializer.save()

            products_data = request.data.get('products', [])
            product_errors = []

            for product_data in products_data:
                product_data['import_list'] = import_list.id

                product_serializer = ImportProductSerializer(data=product_data)
                if product_serializer.is_valid():
                    product_serializer.save()
                else:
                    product_errors.append(product_serializer.errors)

            if product_errors:
                return Response({"product_errors": product_errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response(import_list_serializer.data, status=status.HTTP_201_CREATED)

        return Response(import_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BranchFundTransferListCreateView(ListCreateAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = BranchFundTransfer.objects.all()
    serializer_class = BranchFundTransferSerializer

    filter_backends = [SearchFilter, OrderingFilter, ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BranchFundTransferSerializer
        return BranchFundTransferPostSerializer

    def get_queryset(self):
        return self.queryset.filter(branch=self.request.user.branch)

    def perform_create(self, serializer):
        branch = self.request.user.branch
        serializer.save(
            branch=branch,
            user=self.request.user,
            amount=branch.balance
        )
        wallet = Wallet.objects.last()
        wallet.balance += branch.balance
        wallet.save()
        branch.balance = 0
        branch.save()

class ImportListCreateView(CreateAPIView):
    queryset = ImportList.objects.all()
    serializer_class = ImportListSerializer

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch)


class GiveLendingCreateView(CreateAPIView):
    queryset = Lending.objects.all()
    serializer_class = GivePayLendingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        branch = self.request.user.branch
        serializer.save(
            branch=branch,
            is_lending = True,
        )

class PayLendingCreateView(CreateAPIView):
    queryset = Lending.objects.all()
    serializer_class = GivePayLendingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        branch = self.request.user.branch
        serializer.save(
            branch=branch,
            is_lending=False
        )

class LendingListView(ListAPIView):
    queryset = Lending.objects.all()
    serializer_class = LendingListSerializer


class ExpenseTypeListCreateView(ListCreateAPIView):
    queryset = ExpenseType.objects.all()
    serializer_class = ExpenseTypeSerializer
    permission_classes = [IsAuthenticated]


class ExpenseTypeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ExpenseType.objects.all()
    serializer_class = ExpenseTypeSerializer
    permission_classes = [IsAuthenticated]


class ExpenseListCreateView(ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]


class ExpenseDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]


class SalaryListCreateView(ListCreateAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SalarySerializer
        return SalaryPostSerializer

    def perform_create(self, serializer):
        wallet = Wallet.objects.last()
        branch = self.request.user.branch
        serializer.save(
            branch=branch,
            from_user_id=self.request.user.id,
        )

    def get_queryset(self):
        return self.queryset.filter(
            branch=self.request.user.branch,
        )


class SalaryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [IsAuthenticated]



