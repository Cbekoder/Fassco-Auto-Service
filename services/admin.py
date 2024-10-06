from django.contrib import admin
from .models import Order, OrderService, OrderProduct

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('car_id', 'description', 'total', 'paid', 'landing', 'odo_mileage', 'hev_mileage', 'ev_mileage', 'branch_id', 'created_at')
    search_fields = ('car_id__name', 'description', 'branch_id__name')  # Enable search by car, description, and branch name
    list_filter = ('branch_id', 'created_at')  # Filter by branch and creation date
    ordering = ('-created_at',)  # Order by newest first


@admin.register(OrderService)
class OrderServiceAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'service_id', 'total', 'description')  # Display fields in list view
    search_fields = ('order_id__description', 'service_id__name')  # Search by order description and service name
    list_filter = ('order_id', 'service_id')  # Filter by order and service


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product_id', 'amount', 'total', 'description')  # Display fields in list view
    search_fields = ('order_id__description', 'product_id__name')  # Search by order description and product name
    list_filter = ('order_id', 'product_id')  # Filter by order and product
