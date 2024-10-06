from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('managers/', ManagerListCreateView.as_view(), name='manager-list-create'),
    path('managers/<int:pk>/', ManagerRetrieveUpdateDestroyView.as_view(), name='manager-detail'),
    path('mechanics/', MechanicListCreateView.as_view(), name='mechanic-list-create'),
    path('mechanics/<int:pk>/', MechanicRetrieveUpdateDestroyView.as_view(), name='mechanic-detail'),
    path('workers/', WorkerListCreateView.as_view(), name='other-list-create'),
    path('workers/<int:pk>/', WorkerRetrieveUpdateDestroyView.as_view(), name='other-detail'),
    path('suppliers/', SupplierListCreateView.as_view(), name='supplier_list_create'),
    path('suppliers/<int:pk>/', SupplierRetrieveUpdateDestroyView.as_view(), name='supplier_detail'),
    path('clients/', ClientListCreateView.as_view(), name='client_list_create'),
    path('clients/<int:pk>/', ClientRetrieveUpdateDestroyView.as_view(), name='client_detail'),

]