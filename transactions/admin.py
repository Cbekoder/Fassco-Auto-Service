from django.contrib import admin
from .models import ExpenseType, Expense, Salary, ImportList, ImportProduct, Debt


@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'debt_amount', 'is_debt', 'current_debt', 'branch', 'created_at')
    search_fields = ('supplier__first_name', 'branch__name')
    list_filter = ('branch', 'is_debt', 'created_at')


@admin.register(ExpenseType)
class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch')
    search_fields = ('name', 'branch__name')
    list_filter = ('branch',)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'type', 'amount', 'from_user', 'created_at', 'branch')
    search_fields = ('description', 'type__name', 'from_user__username', 'branch__name')
    list_filter = ('type', 'branch', 'created_at')


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'description', 'amount', 'from_user', 'created_at', 'branch')
    search_fields = ('employee__first_name', 'employee__last_name', 'from_user__username', 'branch__name')
    list_filter = ('branch', 'created_at')


class ImportProductInline(admin.StackedInline):
    model = ImportProduct
    extra = 0

@admin.register(ImportList)
class ImportListAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'total', 'paid', 'debt', 'branch', 'created_at')
    search_fields = ('supplier__first_name', 'branch__name')
    list_filter = ('branch', 'created_at')
    inlines = [ImportProductInline]


@admin.register(ImportProduct)
class ImportProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'amount', 'buy_price', 'total_summ', 'import_list')
    search_fields = ('product__name', 'import_list__branch__name')
    list_filter = ('import_list__branch',)

