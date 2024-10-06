from django.urls import path
from .views import (
    ExpenseTypeListCreateView, ExpenseTypeDetailView, ExpenseListCreateView, ExpenseDetailView,
    SalaryListCreateView, SalaryDetailView, ImportListCreateView, DebtListCreateView, DebtDetailView,
    BranchFundTransferListCreateView, GiveLendingListCreateView, PayLendingListCreateView
)
urlpatterns = [
    path('daily-branch-fund/', BranchFundTransferListCreateView.as_view(), name='daily-branch-fund'),
    path('import/', ImportListCreateView.as_view(), name='import-list-create'),
    path('give-lendings/', GiveLendingListCreateView.as_view(), name='give-lending-list-create'),  # For listing and creating lendings
    path('pay-lendings/', PayLendingListCreateView.as_view(), name='pay-lending-list-create'),  # For listing and creating lendings
    path('expense-types/', ExpenseTypeListCreateView.as_view(), name='expense-type-list-create'),
    path('expense-types/<int:pk>/', ExpenseTypeDetailView.as_view(), name='expense-type-detail'),

    path('expenses/', ExpenseListCreateView.as_view(), name='expense-list-create'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),

    path('salaries/', SalaryListCreateView.as_view(), name='salary-list-create'),
    path('salaries/<int:pk>/', SalaryDetailView.as_view(), name='salary-detail'),

    path('debts/', DebtListCreateView.as_view(), name='debt-list-create'),
    path('debts/<int:pk>/', DebtDetailView.as_view(), name='debt-detail')
]

