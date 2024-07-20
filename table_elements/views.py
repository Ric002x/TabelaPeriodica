from django.http import Http404
from .models import Elements
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
# Create your views here.


def homepageview(request):
    return render(request, 'pages/main_page.html')


class TabelaElementsView(ListView):
    model = Elements
    context_object_name = 'elements'
    template_name = 'pages/table.html'
    ordering = 'id',


class ElementsListView(ListView):
    model = Elements
    context_object_name = 'elements'
    template_name = 'pages/elements_list.html'
    ordering = 'id'
    paginate_by = 18
    paginator_class = Paginator
    page_kwarg = "page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'element_page': True,
            'placeholder_input': 'Procurar um elemento...',
        })
        return context


class SearchElementPageview(ElementsListView):
    template_name = 'pages/elements_list_search.html'

    def get_queryset(self):
        query_set = super().get_queryset()
        search_term = self.request.GET.get('q', '').strip()

        if not search_term:
            raise Http404

        query_set = query_set.filter(
            Q(
                Q(name__icontains=search_term) |
                Q(atomic_number__icontains=search_term)
            ),
        )
        return query_set

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()

        context_data.update({
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
            'element_page': True,
            'placeholder_input': 'Procurar um elemento...',
            'element_page_search': True,
        })

        return context_data


class ElementsDetailView(DetailView):
    model = Elements
    context_object_name = 'element'

    def get_template_names(self):
        slug = self.kwargs.get("slug")
        return [f'partials/element_detail/{slug}.html']
