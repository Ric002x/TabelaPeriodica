from django.test import TestCase
from django.urls import reverse, resolve
from users import views
from users.forms import RegisterForm
# Create your tests here.


class UsersMixin:
    register_form_data = {
        'first_name': 'User',
        'last_name': 'Name',
        'username': 'username',
        'password': 'Password123',
        'password2': 'Password123',
        'email': 'teste@email.com',
    }

    login_form_data = {
        'username': 'username',
        'password': 'Password123',
    }


class UsersAppRegisterTests(TestCase, UsersMixin):
    def setUp(self) -> None:
        self.url_register = reverse('users:register')
        self.url_register_create = reverse('users:register_create')
        return super().setUp()

    # Tests for the Register View/Page
    def test_register_view_function(self):
        view = resolve(self.url_register)
        self.assertEqual(view.func, views.register_view)

    def test_register_view_template(self):
        response = self.client.get(self.url_register)
        self.assertTemplateUsed(response, 'users/pages/register.html')

    def test_register_user_form_sucessful(self):
        response = self.client.post(
            self.url_register_create, data=self.register_form_data,
            follow=True)
        msg = 'usuário cadastrado!'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_register_form_error_password_validations(self):
        self.register_form_data['password2'] = 'DifferentPassword0'
        response = self.client.post(
            self.url_register_create, data=self.register_form_data,
            follow=True
        )
        msg = 'As senhas precisam ser iguais'
        self.assertIn(msg, response.content.decode('utf-8'))

        self.register_form_data['password'] = 'invalidpassword'
        self.register_form_data['password2'] = 'invalidpassword'
        response = self.client.post(
            self.url_register_create, data=self.register_form_data,
            follow=True
        )
        msg = ('A senha deve contar pelo menos 8 caracteres, '
               'incluindo letras maiúsculas e números')
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_register_cant_be_empty_and_min_caracteres(self):
        for key in self.register_form_data:
            self.register_form_data[key] = ''
            response = self.client.post(
                self.url_register_create, data=self.register_form_data,
                follow=True,
            )
            msg = 'Esse campo é obrigatório'
            self.assertIn(msg, response.content.decode('utf-8'))

        self.register_form_data['username'] = 'a'
        response = self.client.post(
                self.url_register_create, data=self.register_form_data,
                follow=True,
            )
        msg = ('Este campo precisa ter '
               'o mínimo de 5 caractéres')
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_register_invalid_email(self):
        self.register_form_data['email'] = 'email'
        response = self.client.post(
                self.url_register_create, data=self.register_form_data,
                follow=True,
            )
        msg = 'Informe um endereço de email válido.'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_register_create_not_post_raise_404(self):
        response = self.client.get(self.url_register_create)
        self.assertEqual(404, response.status_code)


class UsersAppLoginTests(TestCase, UsersMixin):
    def setUp(self) -> None:
        self.url_login = reverse('users:login')
        self.url_login_create = reverse('users:login_create')
        form = RegisterForm(self.register_form_data)
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().setUp()

    def test_login_view_function(self):
        view = resolve(self.url_login)
        self.assertEqual(view.func, views.login_view)

    def test_login_template(self):
        response = self.client.get(self.url_login)
        self.assertTemplateUsed(response, 'users/pages/login.html')

    def test_login_sussesful(self):
        response = self.client.post(
            self.url_login_create, data=self.login_form_data, follow=True,
        )
        msg = 'usuário logado!'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_login_create_raise_404_if_not_post(self):
        response = self.client.get(self.url_login_create)
        self.assertEqual(404, response.status_code)

    def test_login_user_not_found(self):
        self.login_form_data['username'] = 'not_user'
        msg = 'erro no login. confira se o usuário ou senha estão corretos'
        response = self.client.post(
            self.url_login_create, data=self.login_form_data, follow=True,
        )
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_login_invalid_form(self):
        for key in self.login_form_data:
            self.login_form_data[key] = ''
            response = self.client.post(
                self.url_login_create, data=self.login_form_data, follow=True,
            )
            msg = 'erro na validação'
            self.assertIn(msg, response.content.decode('utf-8'))

    def test_redirect_from_login_and_register_if_alread_authenticated(self):
        self.client.post(
            self.url_login_create, data=self.login_form_data, follow=True,
        )
        response_login = self.client.get(self.url_login, follow=True)
        msg = '⚠️ usuário já logado'
        self.assertIn(msg, response_login.content.decode('utf-8'))

        response_register = self.client.get(reverse('users:register'),
                                            follow=True)
        self.assertIn(msg, response_register.content.decode('utf-8'))
