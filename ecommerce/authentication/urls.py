from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login_user/', views.Login.as_view(), name='login_user'),
    path('sign_up/', views.SignUp.as_view(), name='sign_up'),
    path('log_out/', views.Logout.as_view(), name='log_out'),
]
