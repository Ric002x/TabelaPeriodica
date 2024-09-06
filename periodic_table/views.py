from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render

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


def elements_list_view(request):
    search_term = request.GET.get('q', '').strip()
    if search_term:
        query_set = Element.objects.filter(
            Q(
                Q(name__icontains=search_term) |
                Q(atomic_number__icontains=search_term)
            ),
        ).order_by('id')
        paginator = Paginator(object_list=query_set, per_page=18)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(
            request, 'periodic_table/pages/elements_list_search.html',
            context={
                'search_term': search_term,
                'elements': page_obj.object_list,
                'element_page': True,
                'placeholder_input': 'Procurar um elemento...',
                'page_obj': page_obj,
                'element_page_search': True,
            })

    elements = Element.objects.all(
    ).order_by('id')

    if not elements:
        raise Http404

    paginator = Paginator(object_list=elements, per_page=18)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'periodic_table/pages/elements_list.html', context={
        'elements': page_obj.object_list,
        'element_page': True,
        'placeholder_input': 'Procurar um elemento...',
        'page_obj': page_obj,
    })


def element_detail_view(request, slug):
    element = Element.objects.filter(
        slug=slug,
    ).first()
    slug = slug

    if not element:
        raise Http404

    next_element = Element.objects.filter(
        atomic_number__gt=element.atomic_number
    ).order_by('atomic_number').first()

    prev_element = Element.objects.filter(
        atomic_number__lt=element.atomic_number
    ).order_by('-atomic_number').first()

    return render(
        request, 'periodic_table/pages/single_element.html',
        context={
            'element': element,
            'next_element': next_element,
            'prev_element': prev_element
        })


def privacy_police_view(request):
    return render(request, 'periodic_table/pages/privacy_police.html', {
        'privacy_police_page': True,
    })
