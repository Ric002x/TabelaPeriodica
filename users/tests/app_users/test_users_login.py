from django.urls import resolve, reverse

from users import views

from .test_app_users_base import TestBaseUsersApp


class UsersAppLoginTests(TestBaseUsersApp):
    def setUp(self) -> None:
        self.url_login = reverse('users:login')
        self.url_login_create = reverse('users:login_create')
        self.execute_register()
        self.login_form_data = self.generate_form_login()
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
        self.assertTemplateUsed(response, "not_found.html")

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
            msg = 'erro no login. confira se o usuário ou senha estão corretos'
            self.assertIn(msg, response.content.decode('utf-8'))

    def test_redirect_from_login_and_register_if_alread_authenticated(self):
        self.client.post(
            self.url_login_create, data=self.login_form_data, follow=True,
        )
        response_login = self.client.get(self.url_login, follow=True)
        msg = 'usuário já logado'
        self.assertIn(msg, response_login.content.decode('utf-8'))

        response_register = self.client.get(reverse('users:register'),
                                            follow=True)
        self.assertIn(msg, response_register.content.decode('utf-8'))
