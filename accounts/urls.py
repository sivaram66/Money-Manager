from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name= 'logout'),
    path('dashboard/', views.dashboard, name= 'dashboard'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('view_expenses/', views.view_expenses, name='view_expenses'),
    path('manage_budget/', views.manage_budget, name='manage_budget'),
    path('validate-otp/', views.validate_otp, name='validate_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('settings/', views.settings, name='settings'),
    path('reports/', views.reports, name='reports'),


]
