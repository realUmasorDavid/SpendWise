from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.signup, name='register'),
    path('settings/', views.settings, name='settings'),
]
