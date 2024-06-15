from django.urls import path
from . import views

app_name = 'tabela_elementos'

urlpatterns = [
    path('', views.home, name='home'),
    path('tabela/', views.tabela_view, name='tabela'),
    path('elementos/<slug:slug>', views.single_element_view,
         name='single_element'),
]
