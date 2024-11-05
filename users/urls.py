from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from users import views

app_name = 'users'
routers_api = SimpleRouter()
routers_api.register(
    'api',
    views.UsersAPIViewSet,
    basename='users-api'
)

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

    path('esqueci-minha-senha/', views.forgot_my_password,
         name="forgot_my_password"),
    path('redefinir-senha/', views.reset_password,
         name="reset_password"),

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

    # API Urls
    path("api/<str:username>/change-password/",
         views.UsersChangePasswordAPI.as_view(),
         name="change_password_api")

]

urlpatterns += routers_api.urls
