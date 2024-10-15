from django.contrib import admin
from .models import Order, OrderService, OrderProduct

class OrderProductInline(admin.StackedInline):
    model = OrderProduct
    extra = 0

class OrderServiceInline(admin.StackedInline):
    model = OrderService
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('car', 'description', 'total', 'paid', 'landing', 'odo_mileage', 'hev_mileage', 'ev_mileage', 'branch', 'created_at')
    search_fields = ('car__name', 'description', 'branch__name')
    list_filter = ('branch', 'created_at')
    ordering = ('-created_at',)  # Order by newest first
    inlines = [OrderProductInline, OrderServiceInline]


@admin.register(OrderService)
class OrderServiceAdmin(admin.ModelAdmin):
    list_display = ('order', 'service', 'total', 'description')  # Display fields in list view
    search_fields = ('order__description', 'service__name')  # Search by order description and service name
    list_filter = ('order', 'service')  # Filter by order and service


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'amount', 'total', 'description')  # Display fields in list view
    search_fields = ('order__description', 'product__name')  # Search by order description and product name
    list_filter = ('order', 'product')  # Filter by order and product
