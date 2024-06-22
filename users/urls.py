from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('cadastro/', views.RegisterView.as_view(),
         name='register'),
    path('cadastro/criar', views.RegisterView.as_view(),
         name='register_create'),
    path('login/', views.LoginView.as_view(),
         name='login'),
    path('login/logar', views.LoginView.as_view(),
         name='login_create'),
]
