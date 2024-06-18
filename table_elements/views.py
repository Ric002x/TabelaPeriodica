from django.shortcuts import render
from .models import Elements
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator
# Create your views here.


def home(request):
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
    template_name = 'pages/single_element.html'
