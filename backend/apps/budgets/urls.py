from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('create/budgets/', views.budget, name='create_budget'),
    path('budgets/', views.list, name='budget_list'),
    path('budgets/edit/<int:pk>/', views.budget_edit, name='budget_update'),
    path('budgets/delete/<int:pk>/', views.budget_delete, name='budget_delete'),
    # path('budgets/new/', BudgetCreateView.as_view(), name='budget_create'),
    # path('budgets/<int:pk>/edit/', BudgetUpdateView.as_view(), name='budget_update'),
    # path('budgets/<int:pk>/delete/', BudgetDeleteView.as_view(), name='budget_delete'),
    path('update-spending/', views.update_spending, name='update_spending'),
]