from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from . import views

app_name = 'learn_lab'

activity_router_api = SimpleRouter()
activity_router_api.register(
    'api-v2/atividades',
    views.ActivityViewSet,
    basename='activity-api-v2'
)

urlpatterns = [
    path('',
         views.LearnLabListView.as_view(), name='learn_lab_home'),

    path('materia/<str:subject>',
         views.LearnLabSubjectListView.as_view(), name='learn_lab_subject'),

    path('turma/<str:level>',
         views.LearnLabLevelListView.as_view(), name='learn_lab_level'),

    path('atividade/buscar/',
         views.LearnLabListView.as_view(),
         name='learn_lab_activity_search'),

    path('atividade/<slug:slug>',
         views.LearnLabDetailView.as_view(), name='learn_lab_activity'),

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


    # SimpleJWT routs
    path('api/token/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),

    path('api/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),

    path('api/token/verify/',
         TokenVerifyView.as_view(),
         name='token_verify'),


    # Urls for APIs
    path('', include(activity_router_api.urls)),

    path('api-v2/atividades/materia/<int:pk>/',
         views.ActivitiesSubjectListAPIv2.as_view(),
         name='activity-api-v2-subject'),

    path('api-v2/atividades/turma/<int:pk>/',
         views.ActivitiesLevelListAPIv2.as_view(),
         name='activity-api-v2-level')
]
