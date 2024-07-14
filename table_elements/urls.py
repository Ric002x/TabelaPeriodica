from django.urls import path
from . import views

app_name = 'table_elements'

urlpatterns = [
    path('', views.homepageview, name='home'),
    path('tabela/', views.TabelaElementsView.as_view(),
         name='table'),
    path('elementos/buscar-elemento/', views.SearchElementPageview.as_view(),
         name='search_element'),
    path('elementos/lista/', views.ElementsListView.as_view(),
         name='elements_list'),
    path('elementos/<slug:slug>/', views.ElementsDetailView.as_view(),
         name='single_element'),
]
