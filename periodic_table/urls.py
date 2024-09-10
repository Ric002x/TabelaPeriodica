from django.urls import path

from . import views

app_name = 'periodic_table'

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('tabela/', views.table_list_view,
         name='table'),

    path('elementos/buscar-elemento/', views.ElementsListView.as_view(),
         name='search_element'),

    path('elementos/lista/', views.ElementsListView.as_view(),
         name='elements_list'),

    path("api/elementos/", views.ElementsListViewApi.as_view(),
         name="elements_api"),

    path('elementos/<slug:slug>/', views.ElementDetailView.as_view(),
         name='single_element'),

    path('api/elemento/<slug:slug>/', views.ElementDetailViewApi.as_view(),
         name='element_detail_api'),

    path('politicas-de-privacidade', views.privacy_police_view,
         name='privacy_police'),
]
