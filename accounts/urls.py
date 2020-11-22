from django.contrib.auth.views import (LogoutView, PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('change-password/', views.ChangePasswordView.as_view(),
         name='change_password'),

    path('password-reset/', PasswordResetView.as_view(
        template_name='accounts/password_reset.html'),
        name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(
         template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
         template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done', PasswordResetCompleteView.as_view(
         template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),

]
