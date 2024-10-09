from django.contrib import admin
from .models import Order, OrderService, OrderProduct

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('car', 'description', 'total', 'paid', 'landing', 'odo_mileage', 'hev_mileage', 'ev_mileage', 'branch', 'created_at')
    search_fields = ('car__name', 'description', 'branch__name')  # Enable search by car, description, and branch name
    list_filter = ('branch', 'created_at')  # Filter by branch and creation date
    ordering = ('-created_at',)  # Order by newest first


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
