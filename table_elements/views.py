from django.http import Http404
from .models import Elements
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
# Create your views here.


def home_page_view(request):
    return render(request, 'pages/main_page.html', {
        'home_page': True,
    })


def table_list_view(request):
    elements = Elements.objects.filter(
    ).order_by('id')

    return render(request, 'pages/table.html', context={
        'elements': elements,
        'element_page': True,
        'placeholder_input': "Procurar um elemento..."
    })


def elements_list_view(request):
    search_term = request.GET.get('q', '').strip()
    if search_term:
        query_set = Elements.objects.filter(
            Q(
                Q(name__icontains=search_term) |
                Q(atomic_number__icontains=search_term)
            ),
        ).order_by('id')
        paginator = Paginator(object_list=query_set, per_page=18)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'pages/elements_list_search.html', context={
            'search_term': search_term,
            'elements': page_obj.object_list,
            'element_page': True,
            'placeholder_input': 'Procurar um elemento...',
            'page_obj': page_obj,
            'element_page_search': True,
        })

    elements = Elements.objects.all(
    ).order_by('id')

    if not elements:
        raise Http404

    paginator = Paginator(object_list=elements, per_page=18)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/elements_list.html', context={
        'elements': page_obj.object_list,
        'element_page': True,
        'placeholder_input': 'Procurar um elemento...',
        'page_obj': page_obj,
    })


def element_detail_view(request, slug):
    element = Elements.objects.filter(
        slug=slug,
    ).first()
    slug = slug

    if not element:
        raise Http404

    try:
        next_element = Elements.objects.filter(
            atomic_number__gt=element.atomic_number
        ).order_by('atomic_number').first()
    except Elements.DoesNotExist:
        next_element = None

    try:
        prev_element = Elements.objects.filter(
            atomic_number__lt=element.atomic_number
        ).order_by('-atomic_number').first()
    except Elements.DoesNotExist:
        prev_element = None

    return render(request, f'partials/element_detail/{slug}.html', context={
        'element': element,
        'next_element': next_element,
        'prev_element': prev_element
    })
