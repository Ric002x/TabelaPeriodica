from django.urls import path
from rest_framework.routers import SimpleRouter

from users import views

app_name = 'users'
routers_api = SimpleRouter()
routers_api.register(
    'api-v2',
    views.UsersAPIViewSet,
    basename='users-api-v2'
)

print(routers_api.urls)

urlpatterns = [
    path(
        'cadastro/', views.register_view, name='register'),
    path(
        'cadastro/criar', views.register_create, name='register_create'),
    path(
        'login/', views.login_view, name='login'),
    path(
        'login/logar', views.login_create, name='login_create'),
    path(
        'perfil/update', views.perfil_update, name='profile_update'),
    path(
        'perfil/<str:username>/',
        views.profile_user_data, name='profile_data'),
    path('perfil/<str:username>/publicacoes/',
         views.profile_user_posts, name='profile_posts'),
    path('logout/', views.logout_update, name='logout'),
    path('alterar-senha/', views.change_password, name='change_password'),
]

urlpatterns += routers_api.urls
