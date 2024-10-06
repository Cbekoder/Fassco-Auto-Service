from django.contrib import admin
from .models import Product, Service, Car

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'amount', 'unit', 'arrival_price', 'sell_price', 'min_amount', 'max_discount', 'supplier_id', 'branch_id', 'created_at', 'updated_at')
    search_fields = ('code', 'name', 'supplier_id__name')  # Enable search by code, name, and supplier name
    list_filter = ('branch_id', 'created_at', 'updated_at')  # Filter by branch and dates
    ordering = ('-created_at',)  # Order by newest first


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'branch_id')  # Display fields in the list view
    search_fields = ('name',)  # Enable search by name
    list_filter = ('branch_id',)  # Filter by branch


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'color', 'state_number', 'is_sold', 'odo_mileage', 'hev_mileage', 'ev_mileage', 'client_id', 'branch_id', 'created_at')
    search_fields = ('name', 'brand', 'state_number', 'client_id__name')  # Enable search by name, brand, state number, and client name
    list_filter = ('is_sold', 'branch_id', 'created_at')  # Filter by sold status, branch, and creation date
    ordering = ('-created_at',)  # Order by newest first
