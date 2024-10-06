from django.contrib import admin
from .models import ExpenseType, Expense, Salary, ImportList, ImportProduct, Debt

@admin.register(ExpenseType)
class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch_id')
    search_fields = ('name', 'branch_id__name')
    list_filter = ('branch_id',)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'type', 'amount', 'from_user_id', 'created_at', 'branch_id')
    search_fields = ('description', 'type__name', 'from_user_id__username', 'branch_id__name')
    list_filter = ('type', 'branch_id', 'created_at')


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'description', 'amount', 'from_user_id', 'created_at', 'branch_id')
    search_fields = ('employee_id__first_name', 'employee_id__last_name', 'from_user_id__username', 'branch_id__name')
    list_filter = ('branch_id', 'created_at')


@admin.register(ImportList)
class ImportListAdmin(admin.ModelAdmin):
    list_display = ('supplier_id', 'total', 'paid', 'debt', 'branch_id', 'created_at')
    search_fields = ('supplier_id__name', 'branch_id__name')
    list_filter = ('branch_id', 'created_at')


@admin.register(ImportProduct)
class ImportProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'amount', 'buy_price', 'total_summ', 'import_list_id')
    search_fields = ('product_id__name', 'import_list_id__branch_id__name')
    list_filter = ('import_list_id__branch_id',)


@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ('supplier_id', 'debt_amount', 'is_debt', 'current_debt', 'branch_id', 'created_at')
    search_fields = ('supplier_id__name', 'branch_id__name')
    list_filter = ('branch_id', 'is_debt', 'created_at')
