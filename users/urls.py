from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *


urlpatterns = [
    path("get-me/", GetMeAPIView.as_view(), name="get-user"),
    path('employees/', EmployeeListView.as_view(), name='employee_list'),
    path('suppliers/', SupplierListCreateView.as_view(), name='supplier_list_create'),
    path('supplier/<int:pk>/', SupplierRetrieveUpdateDestroyView.as_view(), name='supplier_detail'),
    path('managers/', ManagerListCreateView.as_view(), name='manager-list-create'),
    path('manager/<int:pk>/', ManagerRetrieveUpdateDestroyView.as_view(), name='manager-detail'),
    path('mechanics/', MechanicListCreateView.as_view(), name='mechanic-list-create'),
    path('mechanic/<int:pk>/', MechanicRetrieveUpdateDestroyView.as_view(), name='mechanic-detail'),
    path('workers/', WorkerListCreateView.as_view(), name='other-list-create'),
    path('worker/<int:pk>/', WorkerRetrieveUpdateDestroyView.as_view(), name='other-detail'),
    path('clients/', ClientListCreateView.as_view(), name='client_list_create'),
    path('client/<int:pk>/', ClientRetrieveUpdateDestroyView.as_view(), name='client_detail'),

]