from .test_app_users_base import TestBaseUsersApp
from django.urls import reverse, resolve
from users import views


class UsersAppRegisterTests(TestBaseUsersApp):
    def setUp(self) -> None:
        self.url_register = reverse('users:register')
        self.url_register_create = reverse('users:register_create')
        self.register_form_data = self.generate_form_register()
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

    def test_register_email_already_being_used(self):
        self.client.post(
            self.url_register_create, data=self.register_form_data,
            follow=True)

        response = self.client.post(
            self.url_register_create, data=self.register_form_data,
            follow=True)
        msg = 'invalido. Já existe um usuário cadastrado com esse email'
        self.assertIn(msg, response.content.decode('utf-8'))
