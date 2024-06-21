from django.http import Http404
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.urls import reverse
# Create your views here.


def register_view(request):
    register_form_data = request.session.get('register_form_data, None')
    form = RegisterForm(register_form_data)

    return render(request, 'pages/register.html', context={
        'form': form, 
        'form_action': reverse('users:register_create'),
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

        return redirect('users:login')
    else:
        form = RegisterForm()

    return redirect('users:register')
