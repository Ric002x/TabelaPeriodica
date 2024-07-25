from django.http import Http404
from django.shortcuts import redirect, render
from .forms import RegisterForm, LoginForm, UpdateProfileForm, UpdateUserForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from learn_lab.models import Activity
from django.core.paginator import Paginator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
# Create your views here.


def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, '✅ usuário já logado')
        return redirect('users:profile')

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
        messages.success(request, 'usuário cadastrado!')

        del (request.session['register_form_data'])

        return redirect('users:login')

    else:
        form = RegisterForm()

        messages.error(request, 'erro no cadastro')

        return redirect('users:register')


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, '✅ usuário já logado')
        return redirect('users:profile')

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
            messages.success(request, "usuário logado!")
            login(request, authenticated_user)
            return redirect('learn_lab:learn_lab_home')
        else:
            messages.error(request, 'erro no login. confira '
                           'se o usuário ou senha estão corretos')
            return redirect('users:login')

    else:
        messages.error(request, 'erro na validação')

    return redirect('learn_lab:learn_lab_home')


@login_required(login_url='authors:login', redirect_field_name='next')
def user_manager(request):
    activities = Activity.objects.filter(
        user=request.user,
        is_published=False,
    )
    paginator = Paginator(activities, 9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/profile.html', context={
        'activities': activities,
        'profile_page': True,
        'page_obj': page_obj,
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def perfil_update(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'perfil atualizado com sucesso!')
            return redirect('users:profile')
        else:
            messages.error(request, 'opa! verifique se você'
                           ' preencheu corretamente os campos')

    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

        return render(request, 'pages/profile_update.html', context={
            'user_form': user_form,
            'profile_form': profile_form,
            'form_action': reverse('users:profile_update')
        })


@login_required(login_url='users:login', redirect_field_name='next')
def logout_update(request):
    if not request.POST:
        messages.error(request, 'entre em uma conta para deslogar')
        return redirect(reverse('table_elements:home'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Logout de usuário inválido')
        return redirect(reverse('table_elements:home'))

    logout(request)
    messages.success(request, 'usuário saiu')
    return redirect(reverse('table_elements:home'))


@login_required(login_url='users:login', redirect_field_name='next')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect(reverse('users:profile'))
        else:
            messages.error(request, 'Erro no formulário')

    form = PasswordChangeForm(request.user)

    return render(request, 'pages/change_password.html', context={
        'form': form,
        'form_action': reverse('users:change_password')
    })
