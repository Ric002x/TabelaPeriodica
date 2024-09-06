from django.urls import path

from . import views

app_name = 'learn_lab'

urlpatterns = [
    path('',
         views.lear_lab_list_view, name='learn_lab_home'),
    path('subject/<int:id>',
         views.learn_lab_subject_list_view, name='learn_lab_subject'),
    path('level/<int:id>',
         views.learn_lab_level_list_view, name='learn_lab_level'),
    path('atividade/buscar',
         views.lear_lab_list_view,
         name='learn_lab_activity_search'),
    path('atividade/<slug:slug>',
         views.learn_lab_detail_view, name='learn_lab_activity'),
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
