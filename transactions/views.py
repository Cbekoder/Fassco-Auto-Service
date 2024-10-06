from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from branches.models import Wallet
from users.permissions import IsStaffStatus
from .models import ExpenseType, Expense, Salary, ImportList, ImportProduct, Debt, BranchFundTransfer, Lending
from .serializers import (
    ExpenseTypeSerializer, ExpenseSerializer, SalarySerializer,
    ImportListSerializer, ImportProductSerializer, DebtSerializer,
    BranchFundTransferSerializer, BranchFundTransferPostSerializer, GiveLendingSerializer, LendingListSerializer,
    PayLendingSerializer, SalaryPostSerializer
)

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
        return self.queryset.filter(branch_id=self.request.user.branch)

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


class GiveLendingListCreateView(ListCreateAPIView):
    queryset = Lending.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LendingListSerializer
        return GiveLendingSerializer

    def perform_create(self, serializer):
        branch_id = self.request.user.branch_id
        serializer.save(
            branch_id=branch_id,
            is_lending = True,
        )

    def get_queryset(self):
        return self.queryset.filter(
            branch_id=self.request.user.branch,
            is_lending=True
        )

class PayLendingListCreateView(ListCreateAPIView):
    queryset = Lending.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LendingListSerializer
        return PayLendingSerializer

    def perform_create(self, serializer):
        branch_id = self.request.user.branch_id
        serializer.save(
            branch_id=branch_id,
            is_lending=False
        )

    def get_queryset(self):
        return self.queryset.filter(
            branch_id=self.request.user.branch,
            is_lending=False
        )



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
        branch_id = self.request.user.branch_id
        serializer.save(
            branch_id=branch_id,
            from_user_id=self.request.user.id,
        )

    def get_queryset(self):
        return self.queryset.filter(
            branch_id=self.request.user.branch,
        )


class SalaryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [IsAuthenticated]


class DebtListCreateView(ListCreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
    permission_classes = [IsAuthenticated]


class DebtDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
    permission_classes = [IsAuthenticated]
