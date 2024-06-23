from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
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


class LearnLabActivityView(DetailView):
    model = Activity
    context_object_name = 'activity'
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = 'pages/learn_lab_activity.html'
