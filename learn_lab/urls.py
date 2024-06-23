from django.urls import path
from . import views

app_name = 'learn_lab'

urlpatterns = [
    path('', views.LearnLabHomeView.as_view(), name='learn_lab_home')
]
