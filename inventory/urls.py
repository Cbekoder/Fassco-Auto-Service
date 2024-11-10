from django.urls import path
from .views import ProductListCreateView, ProductRetrieveUpdateDestroyView, ServiceListCreateView, \
    ServiceRetrieveUpdateDestroyView, CarListCreateView, CarRetrieveUpdateDestroyView, TempProductListView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('product-temps/', TempProductListView.as_view(), name='product-list-temp'),
    path('product/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    path('services/', ServiceListCreateView.as_view(), name='service-list-create'),
    path('service/<int:pk>/', ServiceRetrieveUpdateDestroyView.as_view(), name='service-detail'),
    path('cars/', CarListCreateView.as_view(), name='car-list-create'),
    path('car/<int:pk>/', CarRetrieveUpdateDestroyView.as_view(), name='car-detail'),
]
