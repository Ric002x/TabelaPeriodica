from .models import Elements
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator
from django.shortcuts import render
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
    paginate_by = 20
    paginator_class = Paginator
    page_kwarg = "page"


class ElementsDetailView(DetailView):
    model = Elements
    context_object_name = 'element'

    def get_template_names(self):
        slug = self.kwargs.get("slug")
        return [f'partials/element_detail/{slug}.html']
