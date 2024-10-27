from django.urls import path

from . import views

app_name = 'periodic_table'

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('tabela/', views.table_list_view,
         name='table'),

    path('elementos/lista/', views.ElementsListView.as_view(),
         name='elements_list'),

    path('elementos/<slug:slug>/', views.ElementDetailView.as_view(),
         name='single_element'),

    path('politicas-de-privacidade', views.privacy_police_view,
         name='privacy_police'),

    # Url's for API
    path("api/elementos/lista", views.ElementListViewAPI.as_view(),
         name="api_elements_list_view"),

    path("api/elementos/<slug:slug>", views.ElementDetailViewAPI.as_view(),
         name="api_elements_detail_view")
]
