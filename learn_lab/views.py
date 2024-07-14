from typing import Any
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Activity
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.


class LearnLabHomeView(ListView):
    model = Activity
    context_object_name = 'activities'
    ordering = ['-id']
    template_name = 'pages/learn_lab_home.html'
    paginator_class = Paginator
    paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(
            is_published=True,
        )
        return query_set

    def get_context_data(self, **kwargs: Any):
        context_data = super().get_context_data(**kwargs)

        context_data.update({
            'learn_lab_page': True,
            'placeholder_input': 'Buscar por uma atividade...',
        })

        return context_data


class LearnLabActivitySearch(LearnLabHomeView):
    template_name = 'pages/learn_lab_activity_search.html'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()

        if not search_term:
            raise Http404

        query_set = query_set.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            ),
        )
        return query_set

    def get_context_data(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '').strip()

        context = super().get_context_data(*args, **kwargs)

        context.update({
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
            'learn_lab_page': True,
            'placeholder_input': 'Buscar por atividade...'
        })

        return context


class LearnLabActivityView(DetailView):
    model = Activity
    context_object_name = 'activity'
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = 'pages/learn_lab_activitydetail.html'
