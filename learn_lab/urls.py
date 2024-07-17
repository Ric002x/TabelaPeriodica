from django.urls import path
from . import views

app_name = 'learn_lab'

urlpatterns = [
    path('',
         views.LearnLabHomeView.as_view(), name='learn_lab_home'),
    path('atividade/buscar',
         views.LearnLabActivitySearch.as_view(),
         name='learn_lab_activity_search'),
    path('atividade/<slug:slug>',
         views.LearnLabActivityView.as_view(), name='learn_lab_activity'),
    path('atividade/criar/', views.activity_create, name='activity_create')
]
