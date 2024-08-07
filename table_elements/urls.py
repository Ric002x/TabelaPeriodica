from django.urls import path
from . import views

app_name = 'table_elements'

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('tabela/', views.table_list_view,
         name='table'),
    path('elementos/buscar-elemento/', views.elements_list_view,
         name='search_element'),
    path('elementos/lista/', views.elements_list_view,
         name='elements_list'),
    path('elementos/<slug:slug>/', views.element_detail_view,
         name='single_element'),
]
