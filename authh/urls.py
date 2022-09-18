from django.urls import path
from . import views


app_name = 'authh'

urlpatterns = [
    path('accounts/login/', views.LoginView.as_view(), name="login"),
    path('home/', views.Home.as_view(), name="home"),
    path('accounts/logout/', views.logging_out, name="logout"),
    path('accounts/reset_password/', views.reset_password.as_view(), name="reset_password"),
    path('accounts/reset_password_confirm/<str:pk>/', views.confirm.as_view(), name="conf_page"),
    path('accounts/reset_password/success/<str:pk>/', views.reset_pass_success.as_view(), name="reset_pass_success"),
    path('accounts/change_password/', views.change_password.as_view(), name="change_password"),
    path('accounts/change_password_success/', views.change_pass_success.as_view(), name="change_pass_success"),
]
