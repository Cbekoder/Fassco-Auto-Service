from django.contrib import admin
from .models import Product, Service, Car

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('articul', 'name', 'amount', 'unit', 'arrival_price', 'sell_price', 'min_amount', 'max_discount', 'supplier', 'branch', 'created_at', 'updated_at')
    search_fields = ('articul', 'name', 'supplier__first_name')  # Enable search by code, name, and supplier name
    list_filter = ('branch', 'created_at', 'updated_at')  # Filter by branch and dates
    ordering = ('-created_at',)  # Order by newest first


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'branch')  # Display fields in the list view
    search_fields = ('name',)  # Enable search by name
    list_filter = ('branch',)  # Filter by branch


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'color', 'vin_code', 'state_number', 'is_sold', 'odo_mileage', 'hev_mileage', 'ev_mileage', 'client', 'branch', 'created_at')
    search_fields = ('name', 'brand', 'state_number', 'client__first_name')  # Enable search by name, brand, state number, and client name
    list_filter = ('is_sold', 'branch', 'created_at')  # Filter by sold status, branch, and creation date
    ordering = ('-created_at',)  # Order by newest first
