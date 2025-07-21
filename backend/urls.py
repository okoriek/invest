from django.urls import path
from . import views
app_name='backend'

from django.contrib.auth.views import (
    LogoutView, PasswordResetView,
    PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView
)


urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signin/', views.login, name='login'),
    path('signup/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),



    path('verification/<uidb64>/<token>/', views.EmailVerification, name='verification'),
    path('password_reset/', PasswordResetView.as_view(template_name='password/reset_password.html'), name='reset_password'),
    path('password_reset_done/', PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),


]