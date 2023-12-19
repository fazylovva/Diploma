from django.urls import path
from account import views


urlpatterns = [
    path('sign-in', views.SignIn, name='sign-in'),
    path('sign-up', views.SignUp, name='sign-up'),
    path('sign-out', views.SignOut, name='sign-out'),
    path('activate-email', views.ActivateEmail, name='activate-email'),
    path('forgot-password', views.ForgotPassword, name='forgot-password'),
    path('confirm-code', views.ConfirmCode, name='confirm-code'),
    path('reset-password', views.ResetPassword, name='reset-password'),
]
