from django.urls import path

from . import views

app_name = 'periodic_table'

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('tabela/', views.table_list_view,
         name='table'),

    path('elementos/lista/', views.ElementsListView.as_view(),
         name='elements_list'),

    path('elementos/<str:symbol>/', views.ElementDetailView.as_view(),
         name='single_element'),

    path('politicas-de-privacidade/', views.privacy_police_view,
         name='privacy_police'),

    path('api/docs/', views.api_documentation,
         name='api_docs'),

    path('api/docs/elementos/', views.api_documentation_elements,
         name='api_docs_elements'),

    path('api/docs/jwt/', views.api_documentation_jwt,
         name='api_docs_jwt'),

    path('api/docs/usuarios/', views.api_documentation_users,
         name='api_docs_users'),

    path('api/docs/atividades/', views.api_documentation_activities,
         name='api_docs_activities'),

    # Url's for API
    path("api/elementos/", views.ElementListViewAPI.as_view(),
         name="api_elements_list_view"),

    path("api/elementos/<str:symbol>/", views.ElementDetailViewAPI.as_view(),
         name="api_elements_detail_view"),
]
