from django.urls import path
from authors import views

app_name = 'authors'

urlpatterns = [
    path('/', views.author_register_view, name='register')
]
