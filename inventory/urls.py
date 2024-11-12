from django.urls import path
from .views import ProductListView, ProductRetrieveUpdateDestroyView, ServiceListCreateView, \
    ServiceRetrieveUpdateDestroyView, CarListCreateView, CarRetrieveUpdateDestroyView, TempProductListView, \
    TempProductUpdateView, OutOfProductListView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list-create'),
    path('products-out/', OutOfProductListView.as_view(), name='product-list-create'),
    path('product/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    path('product-temps/', TempProductListView.as_view(), name='product-list-temp'),
    path('product-temp/<int:pk>/', TempProductUpdateView.as_view(), name='product-update-temp'),
    path('services/', ServiceListCreateView.as_view(), name='service-list-create'),
    path('service/<int:pk>/', ServiceRetrieveUpdateDestroyView.as_view(), name='service-detail'),
    path('cars/', CarListCreateView.as_view(), name='car-list-create'),
    path('car/<int:pk>/', CarRetrieveUpdateDestroyView.as_view(), name='car-detail'),
]
