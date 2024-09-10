
from typing import Any

from django.db.models import Q
from django.forms import model_to_dict
from django.http import Http404, JsonResponse
from django.http.response import HttpResponse as HttpResponse
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


class ElementsListViewApi(ElementsListView):
    def render_to_response(self, context, **response_kwargs):
        elements = self.get_context_data()['elements']
        elements_list = [{
            'id': element.id,
            'name': element.name,
            "symbol": element.symbol,
            "description": element.description,
            "atomic_number": element.atomic_number,
            "atomic_mass": element.atomic_mass,
            "electrons_number": element.electrons_number,
            "neutrons_number": element.neutrons_number,
            "density": element.density,
            "melting_point": element.melting_point,
            "boiling_point": element.boiling_point,
            "state_matter": element.state_matter,
            "electronic_configuration": element.electronic_configuration,
            "electron_distribution": element.electron_distribution,
            "ionic_states": element.ionic_states,
            "history_and_discovery": element.history_and_discovery,
            "chemical_properties": element.chemical_properties,
            "usage": element.usage,
            "extra_information": element.extra_information,
        }
            for element in elements
        ]
        return JsonResponse(
            elements_list,
            safe=False
        )


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

    def get_context_data(self, **kwargs):
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


class ElementDetailViewApi(ElementDetailView):
    def render_to_response(self, context, **response_kwargs):
        element = self.get_context_data()['element']
        element_dict = model_to_dict(element)

        del element_dict['cover_image']
        del element_dict['bohr_model']

        return JsonResponse(
            element_dict,
            safe=False
        )


def privacy_police_view(request):
    return render(request, 'periodic_table/pages/privacy_police.html', {
        'privacy_police_page': True,
    })
