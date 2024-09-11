from django.urls import path

from . import views

app_name = 'learn_lab'

urlpatterns = [
    path('',
         views.LearnLabListView.as_view(), name='learn_lab_home'),

    path('api/atividades', views.LearnLabListViewApi.as_view(),
         name='activities_api'),

    path('materia/<str:subject>',
         views.LearnLabSubjectListView.as_view(), name='learn_lab_subject'),

    path('turma/<str:level>',
         views.LearnLabLevelListView.as_view(), name='learn_lab_level'),

    path('atividade/buscar/',
         views.LearnLabListView.as_view(),
         name='learn_lab_activity_search'),

    path('atividade/<slug:slug>',
         views.LearnLabDetailView.as_view(), name='learn_lab_activity'),

    path('api/atividade/<slug:slug>', views.LearnLabDetailViewApi.as_view(),
         name='activity_detail_api'),

    path('atividade/criar/',
         views.activity_create, name='activity_create'),

    path('atividade/editar/<slug:slug>',
         views.activity_update, name='activity_update'),

    path('atividade/deletar/<slug:slug>',
         views.activity_delete, name='activity_delete'),

    path('atividade/<slug:slug>/avaliar', views.rating_create,
         name='activity_rate_create'),

    path('atividade/<slug:slug>/editar', views.rating_edit,
         name='activity_rate_edit'),

    path('atividade/<slug:slug>/excluir', views.rating_delete,
         name='activity_rate_delete'),
]
