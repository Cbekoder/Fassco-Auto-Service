from django.urls import path
from .views import (
    OrderListCreateView, OrderRetrieveUpdateDestroyView, 
    OrderServiceListCreateView, OrderServiceRetrieveUpdateDestroyView, 
    OrderProductListCreateView, OrderProductRetrieveUpdateDestroyView
)

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyView.as_view(), name='order-detail'),

    path('order-services/', OrderServiceListCreateView.as_view(), name='order-service-list-create'),
    path('order-services/<int:pk>/', OrderServiceRetrieveUpdateDestroyView.as_view(), name='order-service-detail'),

    path('order-products/', OrderProductListCreateView.as_view(), name='order-product-list-create'),
    path('order-products/<int:pk>/', OrderProductRetrieveUpdateDestroyView.as_view(), name='order-product-detail'),
]
