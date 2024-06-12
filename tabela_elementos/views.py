from django.shortcuts import render
from .models import Elements
from django.http import Http404

# Create your views here.


def home(request):
    return render(request, 'pages/main_page.html')


def tabela_view(request):
    return render(request, 'pages/tabela.html')


def single_element_view(request, slug):
    element = Elements.objects.filter(
        slug=slug,
    )

    if not element:
        raise Http404

    return render(request, 'pages/single_element.html', context={
        'elements': element,
    })
