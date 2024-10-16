from django.urls import path
from .views import *

urlpatterns = [
    path("", BranchBalanceAPIView.as_view(), name="branch-balance"),
]