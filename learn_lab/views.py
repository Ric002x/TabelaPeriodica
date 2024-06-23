from typing import Any
from django.db.models.query import QuerySet
from django.views.generic.list import ListView
from .models import Activity

# Create your views here.


class LearnLabHomeView(ListView):
    model = Activity
    context_object_name = 'activities'
    ordering = ['-id']
    template_name = 'pages/learn_lab_home.html'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(
            is_published=True,
        )
        return query_set
