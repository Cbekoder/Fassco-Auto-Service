from django.urls import path
from .views import OrderListCreateView, OrderDetailView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]