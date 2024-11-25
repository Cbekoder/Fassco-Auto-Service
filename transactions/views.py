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
from django.db.models import Sum, Case, When, F, DecimalField, Value

from branches.models import Wallet
from inventory.models import Product
from services.models import Order, OrderProduct, OrderService
from users.models import Supplier, Client
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
            from_user=self.request.user,
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
            is_lending=True,
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
            branch=self.request.user.branch,
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


# class DetailedBranchStatisticsView(APIView):
#     permission_classes = [IsAdminUser]
#
#     def get(self, request, year=None, month=None, day=None):
#         try:
#             if year and month and day:
#                 start_date = timezone.make_aware(datetime(year, month, day, 0, 0, 0))
#                 end_date = start_date + timedelta(days=1) - timedelta(seconds=1)
#                 duration = "daily"
#             elif year and month:
#                 start_date = timezone.make_aware(datetime(year, month, 1, 0, 0, 0))
#                 if month == 12:
#                     end_date = timezone.make_aware(datetime(year + 1, 1, 1, 0, 0, 0)) - timedelta(seconds=1)
#                 else:
#                     end_date = timezone.make_aware(datetime(year, month + 1, 1, 0, 0, 0)) - timedelta(seconds=1)
#                 duration = "monthly"
#             else:
#                 return Response({"error": "Year and month are required parameters."}, status=400)
#         except ValueError:
#             return Response({"error": "Invalid date format."}, status=400)
#
#         orders = Order.objects.filter(branch=request.user.branch, created_at__range=[start_date, end_date])
#         order_income_details = orders.values("client__first_name").annotate(total_paid=Sum("paid"))
#         order_income_total = orders.aggregate(total=Sum("total"))["total"] or 0
#         order_income_paid = orders.aggregate(total=Sum("paid"))["total"] or 0
#         order_income_landing = orders.aggregate(total=Sum("landing"))["total"] or 0
#
#         order_products = OrderProduct.objects.filter(order__branch=request.user.branch,
#                                                      order__created_at__range=[start_date, end_date])
#         net_selling_product = order_products.aggregate(
#             total_profit=Sum(F("amount") * (F("product__sell_price") - F("product__arrival_price")),
#                              output_field=DecimalField()
#                              ))["total_profit"] or 0
#         total_discounts = order_products.aggregate(
#             total_discount=Sum(
#                 Case(
#                     When(discount_type="%", then=F("total") * F("discount") / Value(100)),
#                     When(discount_type="$", then=F("discount")),
#                     default=Value(0),
#                     output_field=DecimalField()
#                 )
#             )
#         )["total_discount"] or 0
#
#         services = OrderService.objects.filter(
#             order__created_at__range=[start_date, end_date]
#         )
#         service_totals_with_discount = services.annotate(
#             adjusted_total=Case(
#                 When(
#                     discount_type="%",
#                     then=F("total") * (1 - F("discount") / 100)
#                 ),
#                 When(
#                     discount_type="$",
#                     then=F("total") - F("discount")
#                 ),
#                 default=F("total"),
#                 output_field=DecimalField(max_digits=15, decimal_places=2),
#             )
#         ).aggregate(total=Sum("adjusted_total"))["total"] or 0
#
#         # lendings = Lending.objects.filter(branch=request.user.branch, created_at__range=[start_date, end_date], is_lending=False)
#         # lending_income_details = lendings.values("client__first_name").annotate(total_lending=Sum("lending_amount"))
#         # lending_income_total = lendings.aggregate(total=Sum("lending_amount"))["total"] or 0
#
#         incomes = {
#             "order_income": {
#                 "total": order_income_total,
#                 "paid": order_income_paid,
#                 "landing": order_income_landing,
#                 "details": list(order_income_details)
#             },
#             "net_product_profit": net_selling_product - total_discounts,
#             "net_service_profit": service_totals_with_discount,
#             # "client_lending_payments": {
#             #     "total": lending_income_total,
#             #     "details": list(lending_income_details)
#             # },
#             # "total_income": order_income_total + lending_income_total
#             "total_income": order_income_total
#         }
#
#         expenses = Expense.objects.filter(branch=request.user.branch, created_at__range=[start_date, end_date])
#         general_expense_details = expenses.values("type__name").annotate(total_amount=Sum("amount"))
#         general_expense_total = expenses.aggregate(total=Sum("amount"))["total"] or 0
#
#         # salaries = Salary.objects.filter(branch=request.user.branch, created_at__range=[start_date, end_date])
#         # salary_details = salaries.values("employee__first_name").annotate(total_amount=Sum("amount"))
#         # salary_outcome_total = salaries.aggregate(total=Sum("amount"))["total"] or 0
#
#         outcomes = {
#             "expenses": {
#                 "total": general_expense_total,
#                 "details": list(general_expense_details)
#             },
#             # "salaries": {
#             #     "total": salary_outcome_total,
#             #     "details": list(salary_details)
#             # },
#             # "total_outcome": general_expense_total + salary_outcome_total
#             "total_outcome": general_expense_total
#         }
#
#         importList = ImportList.objects.filter(branch=request.user.branch, created_at__range=[start_date, end_date])
#         by_transfer = importList.filter(payment_type="0").aggregate(total_sum=Sum("total"))["total_sum"] or 0
#
#         wareProducts = Product.objects.filter(branch=request.user.branch, is_temp=False)
#         total_warehouse_value = wareProducts.filter(amount__gt=0).aggregate(
#             total_value=Sum(F("amount") * F("sell_price"), output_field=DecimalField()
#                             ))["total_value"] or 0
#
#         supplier_debt_details = Supplier.objects.filter(branch=request.user.branch).values(
#             "first_name", "last_name"
#         ).annotate(
#             total_debt=Sum("debt")
#         )
#         total_supplier_debt = supplier_debt_details.aggregate(total=Sum("total_debt"))["total"] or 0
#
#         debts = Debt.objects.filter(
#             branch=request.user.branch,
#             is_debt=False,
#             created_at__range=[start_date, end_date]
#         )
#         imports = ImportList.objects.filter(
#             branch=request.user.branch,
#             payment_type__isnull=False,
#             is_initial_stock=False,
#             created_at__range=[start_date, end_date]
#         )
#         debt_details = debts.values("supplier__id", "supplier__first_name", "supplier__last_name").annotate(
#             total_paid=Sum("debt_amount")
#         )
#         import_details = imports.values("supplier__id", "supplier__first_name", "supplier__last_name").annotate(
#             total_paid=Sum("paid")
#         )
#
#         supplier_payments = defaultdict(
#             lambda: {"supplier__first_name": "", "supplier__last_name": "", "total_paid": 0})
#
#         for entry in debt_details:
#             supplier_id = entry["supplier__id"]
#             supplier_payments[supplier_id]["supplier__first_name"] = entry["supplier__first_name"]
#             supplier_payments[supplier_id]["supplier__last_name"] = entry["supplier__last_name"]
#             supplier_payments[supplier_id]["total_paid"] += entry["total_paid"]
#
#         for entry in import_details:
#             supplier_id = entry["supplier__id"]
#             supplier_payments[supplier_id]["supplier__first_name"] = entry["supplier__first_name"]
#             supplier_payments[supplier_id]["supplier__last_name"] = entry["supplier__last_name"]
#             supplier_payments[supplier_id]["total_paid"] += entry["total_paid"]
#
#         total_debt_payments = debts.aggregate(total=Sum("debt_amount"))["total"] or 0
#         total_import_payments = imports.aggregate(total=Sum("paid"))["total"] or 0
#         total_paid_to_supplier = total_debt_payments + total_import_payments
#
#         net_income = incomes["total_income"] - outcomes["total_outcome"]
#
#         russian_months = {
#             1: "января", 2: "февраля", 3: "марта", 4: "апреля",
#             5: "мая", 6: "июня", 7: "июля", 8: "августа",
#             9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
#         }
#
#         formatted_start_date = start_date.strftime("%d-%m-%Y")
#         formatted_end_date = end_date.strftime("%d-%m-%Y")
#
#         data = {
#             "branch_id": request.user.branch.id,
#             "duration": duration,
#             "month": russian_months[start_date.month],
#             "start_date": formatted_start_date,
#             "end_date": formatted_end_date,
#             "incomes": incomes,
#             "outcomes": outcomes,
#             "paying_debt": {
#                 "total_paid_to_supplier": total_paid_to_supplier,
#                 "detail": list(supplier_payments.values())
#             },
#             "debt": {
#                 "total": total_supplier_debt,
#                 "detail": list(supplier_debt_details)
#             },
#             "total_by_transfer": by_transfer,
#             "total_warehouse_products": total_warehouse_value,
#             "net_income": net_income
#         }
#
#         return Response(data)
"""
1. Umumiy savdo (order income total)  (mavjud)
2. Import products warehouse (total)  (qo'shish kerak)
3. Import products by_transfer (total) (qo'shish kerak)

4. Servicedan kirim (total) (tushunishimcha mavjud)
5. Sotilgan mahsulot (total sell_price) (qo'shish kerak)
6. Sotilgan tovardan sof foyda (mavjud)

7. Yetkazuvchilardan jami qarzdorlik (mavjud)
8. Yetkazuvchilarga to'landi (mavjud)

9. Mijozlarning umumiy qarzdorligi (qo'shish kerak)

10. Ombordagi warehouse mahsulot (total) (mavjud)
11. Ombordagi warehouse mahsulot (total arrival_price)
12. Ombordagi warehouse mahsulot (total sell_price)

13. Ombordagi by_transfer mahsulot (total) (mavjud)
14. Ombordagi by_transfer mahsulot (total arrival_price)
15. Ombordagi by_transfer mahsulot (total sell_price)
"""


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

        # Calculations
        orders = Order.objects.filter(branch=request.user.branch, created_at__range=[start_date, end_date])

        order_products = OrderProduct.objects.filter(order__branch=request.user.branch,
                                                    order__created_at__range=[start_date, end_date])
        sold_product_total_price = order_products.aggregate(total=Sum(F("amount") * F("product__sell_price"),
                                                                     output_field=DecimalField()))["total"] or 0
        products_totals_with_discount = order_products.annotate(
            adjusted_total=Case(
                When(
                    discount_type="%",
                    then=F("amount") * F("product__sell_price") * (1 - F("discount") / 100)
                ),
                When(
                    discount_type="$",
                    then=F("amount") * (F("product__sell_price") - F("discount"))
                ),
                default=F("amount") * F("product__sell_price"),
                output_field=DecimalField(max_digits=15, decimal_places=2),
            )
        ).aggregate(total=Sum("adjusted_total"))["total"] or 0
        sold_product_net_profit = order_products.aggregate(
            total=Sum(F("amount") * (F("product__sell_price") - F("product__arrival_price")),
                      output_field=DecimalField()))["total"] or 0

        order_services = OrderService.objects.filter(order__branch=request.user.branch,
                                                    order__created_at__range=[start_date, end_date])
        service_income_total = order_services.aggregate(total=Sum("total"))["total"] or 0
        service_totals_with_discount = order_services.annotate(
                        adjusted_total=Case(
                            When(
                                discount_type="%",
                                then=F("total") * (1 - F("discount") / 100)
                            ),
                            When(
                                discount_type="$",
                                then=F("total") - F("discount")
                            ),
                            default=F("total"),
                            output_field=DecimalField(max_digits=15, decimal_places=2),
                        )
                    ).aggregate(total=Sum("adjusted_total"))["total"] or 0
        order_income_total = products_totals_with_discount + service_totals_with_discount

        import_list = ImportList.objects.filter(branch=request.user.branch, created_at__range=[start_date, end_date])
        warehouse_import_total = import_list.exclude(payment_type="0").aggregate(total=Sum("total"))["total"] or 0
        warehouse_import_paid = import_list.exclude(payment_type="0").aggregate(total=Sum("paid"))["total"] or 0

        latest_import_product = ImportProduct.objects.filter(
            import_list__created_at__range=[start_date, end_date],
            import_list__branch=request.user.branch
        ).order_by('-import_list__created_at', '-id').first()

        latest_order_product = OrderProduct.objects.filter(
            order__created_at__range=[start_date, end_date],
            order__branch=request.user.branch
        ).order_by('-order__created_at', '-id').first()

        if latest_import_product and latest_order_product:
            if latest_import_product.import_list.created_at >= latest_order_product.order.created_at:
                latest_warehouse_remainder_sell = latest_import_product.warehouse_remainder_sell_price
                latest_warehouse_remainder_arrival = latest_import_product.warehouse_remainder_arrival_price
            else:
                latest_warehouse_remainder_sell = latest_order_product.warehouse_remainder_sell_price
                latest_warehouse_remainder_arrival = latest_order_product.warehouse_remainder_arrival_price
        elif latest_import_product:
            latest_warehouse_remainder_sell = latest_import_product.warehouse_remainder_sell_price
            latest_warehouse_remainder_arrival = latest_import_product.warehouse_remainder_arrival_price
        elif latest_order_product:
            latest_warehouse_remainder_sell = latest_order_product.warehouse_remainder_sell_price
            latest_warehouse_remainder_arrival = latest_order_product.warehouse_remainder_arrival_price
        else:
            latest_warehouse_remainder_sell = 0
            latest_warehouse_remainder_arrival = 0


        expenses = Expense.objects.filter(branch=request.user.branch, created_at__range=[start_date, end_date])
        general_expense_details = expenses.values("type__name").annotate(total_amount=Sum("amount"))
        general_expense_total = expenses.aggregate(total=Sum("amount"))["total"] or 0

        total_supplier_debt = Supplier.objects.filter(branch=request.user.branch).aggregate(
            total=Sum("debt"))["total"] or 0
        supplier_debt_details = Supplier.objects.filter(branch=request.user.branch).values(
            "first_name", "last_name").annotate(total_debt=Sum("debt")).exclude(total_debt=0)

        total_supplier_payments = Debt.objects.filter(branch=request.user.branch,
                                                      is_debt=False,
                                                      created_at__range=[start_date, end_date]).aggregate(
            total=Sum("debt_amount"))["total"] or 0
        supplier_payment_detail = Debt.objects.filter(branch=request.user.branch,
                                                      is_debt=False,
                                                      created_at__range=[start_date, end_date]).values(
            "supplier__first_name", "supplier__last_name").annotate(total_payment=Sum("debt_amount")).exclude(
            total_payment=0)

        total_client_lending = Client.objects.filter(branch=request.user.branch).aggregate(
            total=Sum("lending"))["total"] or 0
        client_lending_details = Client.objects.filter(branch=request.user.branch).values(
            "first_name", "last_name").annotate(total_lending=Sum("lending")).exclude(total_lending=0)

        warehouse_products = Product.objects.filter(branch=request.user.branch, is_temp=False)
        warehouse_profit = warehouse_products.filter(amount__gt=0).aggregate(
            total_value=Sum(F("amount") * (F("sell_price") - F("arrival_price")), output_field=DecimalField()))["total_value"] or 0
        warehouse_detail = Product.objects.filter(branch=request.user.branch, is_temp=False).values(
            "code", "name").annotate(
            total_value=Sum(F("amount") * F("sell_price"), output_field=DecimalField()),
        ).exclude(total_value=0)
        warehouse_arrival_price = warehouse_products.filter(amount__gt=0).aggregate(
            total_value=Sum(F("amount") * F("arrival_price"), output_field=DecimalField()))["total_value"] or 0
        warehouse_sell_price = warehouse_products.filter(amount__gt=0).aggregate(
            total_value=Sum(F("amount") * F("sell_price"), output_field=DecimalField()))["total_value"] or 0


        import_products = ImportProduct.objects.filter(import_list__branch=request.user.branch,
                                                       import_list__created_at__range=[start_date, end_date])
        not_transfer_products = import_products.exclude(import_list__payment_type="0")
        not_transfer_total_arrival_price = not_transfer_products.aggregate(
                                                total=Sum(F("arrival_price") * F("amount"), output_field=DecimalField()))["total"] or 0
        not_transfer_total_sell_price = not_transfer_products.aggregate(
            total=Sum(F("sell_price") * F("amount"), output_field=DecimalField()))["total"] or 0

        by_transfer_products = import_products.filter(import_list__payment_type="0")
        by_transfer_total_arrival_price = by_transfer_products.aggregate(
            total=Sum(F("arrival_price") * F("amount"), output_field=DecimalField()))["total"] or 0
        by_transfer_total_sell_price = by_transfer_products.aggregate(
            total=Sum(F("sell_price") * F("amount"), output_field=DecimalField()))["total"] or 0

        net_income = order_income_total - (general_expense_total + warehouse_import_paid + total_supplier_payments)

        russian_months = {
            1: "января", 2: "февраля", 3: "марта", 4: "апреля",
            5: "мая", 6: "июня", 7: "июля", 8: "августа",
            9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
        }
        # Response data
        response_data = {
            "branch_id": request.user.branch.id,
            "duration": duration,
            "month": russian_months[start_date.month],
            "start_date": start_date.strftime("%d-%m-%Y"),
            "end_date": end_date.strftime("%d-%m-%Y"),
            "order": {
                "total": order_income_total,
                "products": {
                    "overall_total": sold_product_total_price,
                    "total_with_discount": products_totals_with_discount,
                    "net_profit": sold_product_net_profit
                },
                "services": {
                    "overall_total": service_income_total,
                    "total_with_discount": service_totals_with_discount
                }
            },
            "warehouse_remainder": {
                "sell_price": latest_warehouse_remainder_sell,
                "arrival_price": latest_warehouse_remainder_arrival,
                "net_profit": latest_warehouse_remainder_sell - latest_warehouse_remainder_arrival
            },
            "expenses": {
                "total": general_expense_total,
                "details": list(general_expense_details)
            },
            "debt_from_supplier": {
                "total": total_supplier_debt,
                "detail": list(supplier_debt_details)
            },
            "supplier_payments": {
                "total": total_supplier_payments,
                "detail": list(supplier_payment_detail)
            },
            "client_lending": {
                "total": total_client_lending,
                "detail": list(client_lending_details)
            },
            "warehouse": {
                "arrival_price": warehouse_arrival_price,
                "sell_price": warehouse_sell_price,
                "net_profit": warehouse_profit,
                "detail": warehouse_detail
            },
            "not_transfer": {
                "arrival_price": not_transfer_total_arrival_price,
                "sell_price": not_transfer_total_sell_price,
                "net_profit": not_transfer_total_sell_price - not_transfer_total_arrival_price
            },
            "by_transfer": {
                "arrival_price": by_transfer_total_arrival_price,
                "sell_price": by_transfer_total_sell_price,
                "net_profit": by_transfer_total_sell_price - by_transfer_total_arrival_price
            },
            "net_income": net_income
        }

        return Response(response_data)
