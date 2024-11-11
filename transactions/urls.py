from django.urls import path
from .views import (
    ExpenseTypeListCreateView, ExpenseTypeDetailView, ExpenseListCreateView, ExpenseDetailView,
    SalaryListCreateView, SalaryDetailView, ImportCreateView, DebtListView, DebtDetailView,
    BranchFundTransferListCreateView, GiveLendingCreateView, PayLendingCreateView, GetDebtCreateView,
    PayDebtCreateView, ImportListAPIView, ImportListDetailAPIView, LendingListView, LendingDetailView,
    DetailedBranchStatisticsView
)
urlpatterns = [
    path('debt-get/', GetDebtCreateView.as_view(), name='get-debt'),
    path('debt-pay/', PayDebtCreateView.as_view(), name='get-debt'),
    path('debts/', DebtListView.as_view(), name='debt-list-create'),
    path('debt/<int:pk>/', DebtDetailView.as_view(), name='debt-detail'),
    path('daily-branch-fund/', BranchFundTransferListCreateView.as_view(), name='daily-branch-fund'),
    path('import/', ImportCreateView.as_view(), name='import-list-create'),
    path('import-lists/', ImportListAPIView.as_view(), name='import-list'),
    path('import-list/<int:pk>/', ImportListDetailAPIView.as_view(), name='import-list-detail'),
    path('lending-give/', GiveLendingCreateView.as_view(), name='give-lending-list-create'),  # For listing and creating lendings
    path('lending-pay/', PayLendingCreateView.as_view(), name='pay-lending-list-create'),  # For listing and creating lendings
    path('lendings/', LendingListView.as_view(), name='lending-list-create'),  # For listing and creating lendings
    path('lending/<int:pk>', LendingDetailView.as_view(), name='lending-update-delete'),  # For listing and creating lendings
    path('expense-types/', ExpenseTypeListCreateView.as_view(), name='expense-type-list-create'),
    path('expense-type/<int:pk>/', ExpenseTypeDetailView.as_view(), name='expense-type-detail'),
    path('expenses/', ExpenseListCreateView.as_view(), name='expense-list-create'),
    path('expense/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
    path('salaries/', SalaryListCreateView.as_view(), name='salary-list-create'),
    path('salary/<int:pk>/', SalaryDetailView.as_view(), name='salary-detail'),
    path('statistics/<str:duration>/', DetailedBranchStatisticsView.as_view(), name='statistics'),
    path('statistics/<str:duration>/<str:start_date>/<str:end_date>/', DetailedBranchStatisticsView.as_view(), name='statistics'),
]

