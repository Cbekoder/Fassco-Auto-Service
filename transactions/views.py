from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
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
    GetPayDebtSerializer, GivePayLendingSerializer, DebtUpdateSerializer, GetImportListSerializer,
    LendingUpdateSerializer, SalaryUpdateSerializer
)


class GetDebtCreateView(CreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = GetPayDebtSerializer
    permission_classes = (IsAuthenticated,)
    
    def perform_create(self, serializer):
        branch = self.request.user.branch
        debt_amount = serializer.validated_data.get('debt_amount', 0)
        supplier = serializer.validated_data.get('supplier')
        current_debt = supplier.debt + debt_amount

        serializer.save(
            branch=branch,
            is_debt=True,
            current_debt=current_debt,
        )

class PayDebtCreateView(CreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = GetPayDebtSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        branch = self.request.user.branch
        debt_amount = serializer.validated_data.get('debt_amount', 0)
        supplier = serializer.validated_data.get('supplier')
        current_debt = supplier.debt - debt_amount
        if branch.balance < debt_amount:
            raise ValidationError({'detail':"Paid amount cannot be greater than branch balance"})
        if debt_amount > supplier.debt:
            raise ValidationError({'detail':"Debt amount cannot be greater than supplier debt"})
        serializer.save(
            branch=branch,
            is_debt=False,
            current_debt=current_debt,
        )

class DebtListView(ListAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='is_debt',
                in_=openapi.IN_QUERY,
                description="Filter by whether it's a debt (true or false)",
                type=openapi.TYPE_BOOLEAN
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = self.queryset.filter(branch=self.request.user.branch)
            is_debt = self.request.query_params.get('is_debt')

            if is_debt is not None:
                if is_debt.lower() == 'true':
                    queryset = queryset.filter(is_debt=True)
                elif is_debt.lower() == 'false':
                    queryset = queryset.filter(is_debt=False)

            return queryset
        return self.queryset.none()

class DebtDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()

class ExpenseTypeListCreateView(ListCreateAPIView):
    queryset = ExpenseType.objects.all()
    serializer_class = ExpenseTypeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            branch=self.request.user.branch
        )

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()


class ExpenseTypeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ExpenseType.objects.all()
    serializer_class = ExpenseTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset


class ExpenseListCreateView(ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()

    def perform_create(self, serializer):
        serializer.save(
            from_user = self.request.user,
            branch=self.request.user.branch
        )


class ExpenseDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()


class ImportCreateView(APIView):
    @swagger_auto_schema(
        request_body=ImportListSerializer,
        responses={201: ImportListSerializer, 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = ImportListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(branch=self.request.user.branch)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImportListAPIView(ListAPIView):
    queryset = ImportList.objects.all()
    serializer_class = ImportListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetImportListSerializer
        return ImportListSerializer

class ImportListDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ImportList.objects.all()
    serializer_class = ImportListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()


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
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()

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


class GiveLendingCreateView(CreateAPIView):
    queryset = Lending.objects.all()
    serializer_class = GivePayLendingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        branch = self.request.user.branch
        lending_amount = serializer.validated_data.get('lending_amount', 0)
        client = serializer.validated_data.get('client')
        current_lending = client.lending + lending_amount
        serializer.save(
            branch=branch,
            is_lending = True,
            current_lending=current_lending
        )

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()

class PayLendingCreateView(CreateAPIView):
    queryset = Lending.objects.all()
    serializer_class = GivePayLendingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        branch = self.request.user.branch
        lending_amount = serializer.validated_data.get('lending_amount', 0)
        client = serializer.validated_data.get('client')
        current_lending = client.lending - lending_amount
        serializer.save(
            branch=branch,
            is_lending=False,
            current_lending=current_lending
        )

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()

class LendingListView(ListAPIView):
    queryset = Lending.objects.all()
    serializer_class = LendingListSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='is_lending',
                in_=openapi.IN_QUERY,
                description="Filter by whether it's a lending (true or false)",
                type=openapi.TYPE_BOOLEAN
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = self.queryset.filter(branch=self.request.user.branch)
            is_lending = self.request.query_params.get('is_debt')

            if is_lending is not None:
                if is_lending.lower() == 'true':
                    queryset = queryset.filter(is_lending=True)
                elif is_lending.lower() == 'false':
                    queryset = queryset.filter(is_lending=False)

            return queryset
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()

class LendingDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Lending.objects.all()
    serializer_class = LendingUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()


class SalaryListCreateView(ListCreateAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            branch= self.request.user.branch,
            from_user=self.request.user,
        )

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()


class SalaryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalaryUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()



