from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('cadastro/', views.register_view, name='register'),
    path('cadastro/criar', views.register_create, name='register_create')
]
