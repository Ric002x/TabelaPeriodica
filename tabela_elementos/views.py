from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'pages/main_page.html')


def tabela_view(request):
    return render(request, 'pages/tabela.html')


def single_element_view(request):
    return render(request, 'pages/sigle_element')
