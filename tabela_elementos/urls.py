from django.urls import path
from . import views

app_name = 'tabela_elementos'

urlpatterns = [
    path('', views.home),
    path('tabela/', views.tabela_view, name='tabela'),
    # path('elementos/<slug:slug>', name='single_element'),
]
