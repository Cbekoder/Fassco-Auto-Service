from collections import defaultdict
from decimal import Decimal

from drf_yasg import openapi
from django.utils import timezone
from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Q, F, DecimalField

from branches.models import Wallet
from inventory.models import Product
from services.models import Order
from users.models import Supplier
from users.permissions import IsAdminUser
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
    permission_classes = (IsAdminUser,)

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
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        branch = self.request.user.branch
        debt_amount = serializer.validated_data.get('debt_amount', 0)
        supplier = serializer.validated_data.get('supplier')
        current_debt = supplier.debt - debt_amount
        serializer.save(
            branch=branch,
            is_debt=False,
            current_debt=current_debt,
        )

class DebtListView(ListAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
    permission_classes = [IsAdminUser]

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
            queryset = self.queryset.filter(branch=self.request.user.branch).order_by('-created_at')
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
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()

class ExpenseTypeListCreateView(ListCreateAPIView):
    queryset = ExpenseType.objects.all()
    serializer_class = ExpenseTypeSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(
            branch=self.request.user.branch
        )

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch).order_by('-id')
        return self.queryset.none()


class ExpenseTypeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ExpenseType.objects.all()
    serializer_class = ExpenseTypeSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset

class ExpenseListCreateView(ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch).order_by('-created_at')
        return self.queryset.none()

    def perform_create(self, serializer):
        serializer.save(
            from_user = self.request.user,
            branch=self.request.user.branch
        )


class ExpenseDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAdminUser]

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
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch).order_by('-created_at')
        return self.queryset.none()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetImportListSerializer
        return ImportListSerializer

class ImportListDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ImportList.objects.all()
    serializer_class = GetImportListSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch).order_by('-created_at')
        return self.queryset.none()


class BranchFundTransferListCreateView(ListCreateAPIView):
    permission_classes = (IsAdminUser,)

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


class GiveLendingCreateView(CreateAPIView):
    queryset = Lending.objects.all()
    serializer_class = GivePayLendingSerializer
    permission_classes = [IsAdminUser]

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
    permission_classes = [IsAdminUser]

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
    permission_classes = [IsAdminUser]

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
            queryset = self.queryset.filter(branch=self.request.user.branch).order_by('-created_at')
            is_lending = self.request.query_params.get('is_debt')

            if is_lending is not None:
                if is_lending.lower() == 'true':
                    queryset = queryset.filter(is_lending=True)
                elif is_lending.lower() == 'false':
                    queryset = queryset.filter(is_lending=False)

            return queryset
        return self.queryset.none()

class LendingDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Lending.objects.all()
    serializer_class = LendingUpdateSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()


class SalaryListCreateView(ListCreateAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(
            branch= self.request.user.branch,
            from_user=self.request.user,
        )

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch).order_by('-created_at')
        return self.queryset.none()


class SalaryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalaryUpdateSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()


class DetailedBranchStatisticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, year=None, month=None, day=None):
        try:
            if year and month and day:
                start_date = timezone.make_aware(datetime(year, month, day, 0, 0, 0))
                end_date = start_date + timedelta(days=1) - timedelta(seconds=1)
                duration = "daily"
            elif year and month:
                start_date = timezone.make_aware(datetime(year, month, 1, 0, 0, 0))
                if month == 12:
                    end_date = timezone.make_aware(datetime(year + 1, 1, 1, 0, 0, 0)) - timedelta(seconds=1)
                else:
                    end_date = timezone.make_aware(datetime(year, month + 1, 1, 0, 0, 0)) - timedelta(seconds=1)
                duration = "monthly"
            else:
                return Response({"error": "Year and month are required parameters."}, status=400)
        except ValueError:
            return Response({"error": "Invalid date format."}, status=400)

        orders = Order.objects.filter(branch=request.user.branch, created_at__range=[start_date, end_date])
        order_income_details = orders.values("client__first_name").annotate(total_paid=Sum("paid"))
        order_income_total = orders.aggregate(total=Sum("total"))["total"] or 0
        order_income_paid = orders.aggregate(total=Sum("paid"))["total"] or 0
        order_income_landing = orders.aggregate(total=Sum("landing"))["total"] or 0

        lendings = Lending.objects.filter(branch=request.user.branch, created_at__range=[start_date, end_date], is_lending=False)
        lending_income_details = lendings.values("client__first_name").annotate(total_lending=Sum("lending_amount"))
        lending_income_total = lendings.aggregate(total=Sum("lending_amount"))["total"] or 0

        incomes = {
            "order_income": {
                "total": order_income_total,
                "paid": order_income_paid,
                "landing": order_income_landing,
                "details": list(order_income_details)
            },
            "client_lending_payments": {
                "total": lending_income_total,
                "details": list(lending_income_details)
            },
            "total_income": order_income_total + lending_income_total
        }

        expenses = Expense.objects.filter(branch=request.user.branch, created_at__range=[start_date, end_date])
        general_expense_details = expenses.values("type__name").annotate(total_amount=Sum("amount"))
        general_expense_total = expenses.aggregate(total=Sum("amount"))["total"] or 0

        # salaries = Salary.objects.filter(branch=request.user.branch, created_at__range=[start_date, end_date])
        # salary_details = salaries.values("employee__first_name").annotate(total_amount=Sum("amount"))
        # salary_outcome_total = salaries.aggregate(total=Sum("amount"))["total"] or 0

        outcomes = {
            "expenses": {
                "total": general_expense_total,
                "details": list(general_expense_details)
            },
            # "salaries": {
            #     "total": salary_outcome_total,
            #     "details": list(salary_details)
            # },
            # "total_outcome": general_expense_total + salary_outcome_total
            "total_outcome": general_expense_total
        }

        importList = ImportList.objects.filter(branch=request.user.branch, created_at__range=[start_date, end_date])
        by_transfer = importList.filter(payment_type="0").aggregate(total_sum=Sum("total"))["total_sum"] or 0

        wareProducts = Product.objects.filter(branch=request.user.branch, is_temp=False)
        total_warehouse_value = wareProducts.filter(amount__gt=0).aggregate(
            total_value=Sum(F("amount") * F("sell_price"), output_field=DecimalField()
                            ))["total_value"] or 0

        supplier_debt_details = Supplier.objects.filter(branch=request.user.branch).values(
            "first_name", "last_name"
        ).annotate(
            total_debt=Sum("debt")
        )
        total_supplier_debt = supplier_debt_details.aggregate(total=Sum("total_debt"))["total"] or 0

        debts = Debt.objects.filter(
            branch=request.user.branch,
            is_debt=False,
            created_at__range=[start_date, end_date]
        )
        imports = ImportList.objects.filter(
            branch=request.user.branch,
            payment_type__isnull=False,
            is_initial_stock=False,
            created_at__range=[start_date, end_date]
        )
        debt_details = debts.values("supplier__id", "supplier__first_name", "supplier__last_name").annotate(
            total_paid=Sum("debt_amount")
        )
        import_details = imports.values("supplier__id", "supplier__first_name", "supplier__last_name").annotate(
            total_paid=Sum("paid")
        )

        supplier_payments = defaultdict(
            lambda: {"supplier__first_name": "", "supplier__last_name": "", "total_paid": 0})

        for entry in debt_details:
            supplier_id = entry["supplier__id"]
            supplier_payments[supplier_id]["supplier__first_name"] = entry["supplier__first_name"]
            supplier_payments[supplier_id]["supplier__last_name"] = entry["supplier__last_name"]
            supplier_payments[supplier_id]["total_paid"] += entry["total_paid"]

        for entry in import_details:
            supplier_id = entry["supplier__id"]
            supplier_payments[supplier_id]["supplier__first_name"] = entry["supplier__first_name"]
            supplier_payments[supplier_id]["supplier__last_name"] = entry["supplier__last_name"]
            supplier_payments[supplier_id]["total_paid"] += entry["total_paid"]

        total_debt_payments = debts.aggregate(total=Sum("debt_amount"))["total"] or 0
        total_import_payments = imports.aggregate(total=Sum("paid"))["total"] or 0
        total_paid_to_supplier = total_debt_payments + total_import_payments

        net_income = incomes["total_income"] - outcomes["total_outcome"]

        formatted_start_date = start_date.strftime("%d-%m-%Y")
        formatted_end_date = end_date.strftime("%d-%m-%Y")

        data = {
            "branch_id": request.user.branch.id,
            "duration": duration,
            "start_date": formatted_start_date,
            "end_date": formatted_end_date,
            "incomes": incomes,
            "outcomes": outcomes,
            "paying_debt": {
                "total_paid_to_supplier": total_paid_to_supplier,
                "detail": list(supplier_payments.values())
            },
            "debt": {
                "total": total_supplier_debt,
                "detail": list(supplier_debt_details)
            },
            "total_by_transfer": by_transfer,
            "total_warehouse_products": total_warehouse_value,
            "net_income": net_income
        }

        return Response(data)

