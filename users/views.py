from django.http import Http404
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
# Create your views here.


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    return render(request, 'pages/register.html', context={
        'form': form,
        'form_action': reverse('users:register_create'),
        'register_page': True,
    })


def register_create(request):
    if not request.POST:
        raise Http404

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        del (request.session['register_form_data'])

        messages.success(request, 'Usuário Criado')
        return redirect('users:login')
    else:
        messages.error(request, 'Erro no cadastro')
        return redirect('users:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'pages/login.html', context={
        'form': form,
        'form_action': reverse('users:login_create'),
        'login_page': True,
    })


def login_create(request):
    if not request.POST:
        raise Http404

    form = LoginForm(request.POST)
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, "Logado com sucesso")
            login(request, authenticated_user)
        else:
            messages.error(request, 'Nome de usuário ou senha '
                           'podem estar incorretos')
            return redirect('users:login')

    return redirect('table_elements:home')
