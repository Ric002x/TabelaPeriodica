from django.http import Http404
from django.shortcuts import redirect
from .forms import RegisterForm, LoginForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView

# Create your views here.


class RegisterView(FormView):
    template_name = 'pages/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:login')

    def get_initial(self):
        initial = super().get_initial()
        register_form_data = self.request.session.get(
            'register_form_data', None)
        if register_form_data:
            initial.update(register_form_data)
        return initial

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        if 'register_form_data' in self.request.session:
            del self.request.session['register_form_data']
        messages.success(self.request, 'Usuário criado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Salva os dados do formulário na sessão e mostra uma mensagem de erro
        self.request.session['register_form_data'] = self.request.POST
        messages.error(self.request, 'Erro no cadastro')
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        if request.method != 'POST':
            raise Http404

        POST = request.POST
        request.session['register_form_data'] = POST
        form = self.get_form(self.form_class)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        # Adiciona contexto adicional à renderização do template
        context = super().get_context_data(**kwargs)
        context['form_action'] = reverse_lazy('users:register_create')
        context['register_page'] = True
        return context


class LoginView(FormView):
    template_name = 'pages/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('table_elements:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_action'] = reverse_lazy('users:login_create')
        context['login_page'] = True
        return context

    def form_valid(self, form):
        username = form.cleaned_data.get('username', '')
        password = form.cleaned_data.get('password', '')
        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is not None:
            login(self.request, authenticated_user)
            messages.success(self.request, "Logado com sucesso")
            return super().form_valid(form)
        else:
            messages.error(self.request,
                           'Nome de usuário ou senha podem estar incorretos')
            return redirect('users:login')

    def form_invalid(self, form):
        messages.error(self.request, 'Erro no formulário de login')
        return redirect('users:login')

    def post(self, request, *args, **kwargs):
        if request.method != 'POST':
            raise Http404

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
