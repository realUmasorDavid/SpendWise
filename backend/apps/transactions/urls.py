from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_transaction, name='create_transaction'),
    path('create/category/', views.create_category, name='create_category'),
]
