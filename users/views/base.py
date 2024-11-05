from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from learn_lab.models import Activity

from ..forms import (LoginForm, RegisterForm, ResetPasswordForm,
                     UpdateProfileForm, UpdateUserForm)

token_password = PasswordResetTokenGenerator()


def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, 'usuário já logado')
        return redirect(reverse(
            'users:profile_posts',
            kwargs={'username': request.user}))

    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    return render(request, 'users/pages/register.html', context={
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
        messages.warning(request, 'usuário já logado')
        return redirect(reverse(
            'users:profile_posts',
            kwargs={'username': request.user}))

    form = LoginForm()
    return render(request, 'users/pages/login.html', context={
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

    messages.error(request, 'erro no login. confira '
                   'se o usuário ou senha estão corretos')
    return redirect('users:login')


@login_required(login_url='users:login', redirect_field_name='next')
def profile_user_data(request, username):
    try:
        profile_user = get_object_or_404(User, username=username)
    except User.DoesNotExist:
        raise Http404

    if profile_user == request.user:
        return render(request, 'users/pages/profile.html', context={
            'profile_user_data': True,
            'profile_user': profile_user
        })
    else:
        messages.error(
            request, "Ainda não está disponível a \
                visualização de outro perfil")
        return redirect(reverse('periodic_table:home'))


@login_required(login_url='users:login', redirect_field_name='next')
def profile_user_posts(request, username):
    try:
        profile_user = get_object_or_404(User, username=username)
    except User.DoesNotExist:
        raise Http404

    if profile_user == request.user:
        activities = Activity.objects.filter(
            user=profile_user,
        ).order_by('is_published').select_related('level', 'subject')

        paginator = Paginator(activities, 9)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'users/pages/profile.html', context={
            'activities': page_obj.object_list,
            'profile_user_posts': True,
            'page_obj': page_obj,
            'profile_user': profile_user,
        })
    else:
        messages.error(
            request, "Ainda não está disponível a \
                visualização de outro perfil")
        return redirect(reverse('periodic_table:home'))


@login_required(login_url='users:login', redirect_field_name='next')
def perfil_update(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'perfil atualizado com sucesso!')
            return redirect(
                reverse('users:profile_data',
                        kwargs={'username': request.user}))
        else:
            messages.error(request, 'opa! verifique se você'
                           ' preencheu corretamente os campos')
            return redirect(reverse('users:profile_update'))

    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

        return render(request, 'users/pages/profile_update.html', context={
            'user_form': user_form,
            'profile_form': profile_form,
            'form_action': reverse('users:profile_update')
        })


@login_required(login_url='users:login', redirect_field_name='next')
def logout_update(request):
    if not request.POST:
        messages.warning(request, 'Logout Inválido')
        return redirect(reverse('periodic_table:home'))

    if request.POST.get('username') != request.user.username:
        messages.warning(request, 'Logout inválido')
        return redirect(reverse('periodic_table:home'))

    logout(request)
    messages.success(request, 'Usuário desconectado')
    return redirect(reverse('periodic_table:home'))


@login_required(login_url='users:login', redirect_field_name='next')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect(reverse(
                'users:profile_posts',
                kwargs={'username': request.user}))
        else:
            messages.error(request, 'Erro no formulário')
            redirect(reverse('users:change_password'))

    form = PasswordChangeForm(request.user)

    return render(request, 'users/pages/change_password.html', context={
        'form': form,
        'form_action': reverse('users:change_password'),
        'change_password': True
    })


def forgot_my_password(request):
    if request.user.is_authenticated:
        messages.warning(request, 'usuário já logado')
        return redirect(reverse(
            'users:profile_posts',
            kwargs={'username': request.user}))

    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            messages.error(request, "Por favor, insira um e-mail válido.")
            return redirect("users:forgot_my_password")

        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = token_password.make_token(user)
            reset_link = request.build_absolute_uri(
                reverse("users:reset_password", kwargs={
                        "uidb64": uid, 'token': token})
            )

            mail = EmailMultiAlternatives(
                subject="Solicitação de Alteração de Senha",
                body=(
                    "Houve uma solicitação de redefinição de senha para o"
                    " seu cadastro no site:\n"
                    "atomicdiscoveries.ricardovenicius.com.br.\n\n"

                    "Para continuar com a solicitação, clique no link abaixo"
                    " para seguir com a redefinição de senha:\n"
                    f"{reset_link}\n\n"

                    "Este link tem uma validade de 5 minutos, após passado"
                    " esse tempo, será necessário fazer uma nova solicitação."

                    "\n\nCaso não tenha solicitado esta alteração, ignore este"
                    " e-mail e sua senha permanecerá a mesma.\n\n"

                    "Atenciosamente,\n\n"
                    "Equipe de Suporte"
                ),
                from_email="no-reply@em704.ricardovenicius.com.br",
                to=[email],
            )
            mail.send()
            messages.success(request, "Solicitação enviada! Verifique seu"
                             " e-mail para o link de redefinição de senha")
            return redirect("users:forgot_my_password")

        except User.DoesNotExist:
            messages.error(request, "Falha na solicitação!"
                           " Certifique-se que solicitou para o email correto")
            return redirect("users:forgot_my_password")

        except Exception as e:
            messages.error(request, f"Falha na solicitação!: {e}")
            return redirect("users:forgot_my_password")

    return render(request, "users/pages/forgot_my_password.html", context={
        "form_action": reverse("users:forgot_my_password")
    })


def reset_password(request, uidb64, token):
    if request.user.is_authenticated:
        messages.warning(request, 'usuário já logado')
        return redirect(reverse(
            'users:profile_posts',
            kwargs={'username': request.user}))

    uid = urlsafe_base64_decode(uidb64).decode()
    user = User.objects.get(pk=uid)

    if user is None or not token_password.check_token(user, token):
        messages.error(
            request, "O link de redefinição de senha é inválido ou expirou.")
        return redirect("users:forgot_my_password")

    elif user is not None:
        if request.method == "POST":
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data.get('new_password')
                user.set_password(new_password)
                user.save()
                messages.success(
                    request, "Senha redefinida com sucesso."
                    " Faça login para continuar")
                return redirect("users:login")
            else:
                messages.error(request, "Erro na alteração de senha")
                return render(
                    request, 'users/pages/reset_password.html', {
                        'form': form,
                        'form_action': reverse(
                            "users:reset_password",
                            kwargs={"uidb64": uidb64, 'token': token})
                    })

        form = ResetPasswordForm()
        return render(
            request, 'users/pages/reset_password.html', {
                'form': form,
                'form_action': reverse(
                    "users:reset_password",
                    kwargs={"uidb64": uidb64, 'token': token})
            })

    else:
        messages.error(
            request, "Link inválido ou expirado. Por favor, tente novamente")
        return redirect("users:forgot_my_password")
