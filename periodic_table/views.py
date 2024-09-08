from typing import Any

from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import Element

# Create your views here.


def home_page_view(request):
    return render(request, 'periodic_table/pages/main_page.html', {
        'home_page': True,
    })


def table_list_view(request):
    elements = Element.objects.filter(
    ).order_by('id')

    return render(request, 'periodic_table/pages/table.html', context={
        'elements': elements,
        'element_page': True,
        'placeholder_input': "Procurar um elemento..."
    })


class ElementsListView(ListView):
    model = Element
    paginate_by = 18
    template_name = "periodic_table/pages/elements_list.html"
    context_object_name = "elements"
    ordering = ['id']

    def get_queryset(self):
        search_term = self.request.GET.get('q', '').strip()
        if search_term:
            return Element.objects.filter(
                Q(name__icontains=search_term) |
                Q(atomic_number__icontains=search_term)
            ).order_by('id')

        return Element.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_term = self.request.GET.get('q', '').strip()
        context.update({
            'search_term': search_term,
            'element_page': True,
            'placeholder_input': 'Procurar um elemento...',
            'element_page_search': bool(search_term),
        })
        return context


class ElementDetailView(DetailView):
    model = Element
    template_name = 'periodic_table/pages/single_element.html'
    context_object_name = "element"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        try:
            element = Element.objects.get(slug=self.kwargs.get('slug'))
        except Element.DoesNotExist:
            raise Http404
        return element

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        element = self.get_object()

        next_element = Element.objects.filter(
            atomic_number__gt=element.atomic_number
        ).order_by('atomic_number').first()

        # Elemento anterior com atomic_number menor
        prev_element = Element.objects.filter(
            atomic_number__lt=element.atomic_number
        ).order_by('-atomic_number').first()

        context.update({
            'next_element': next_element,
            'prev_element': prev_element,
        })
        return context


def privacy_police_view(request):
    return render(request, 'periodic_table/pages/privacy_police.html', {
        'privacy_police_page': True,
    })
