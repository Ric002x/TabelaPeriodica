from django.urls import resolve, reverse

from users import views

from .test_app_users_base import TestBaseUsersApp


class UsersAppProfilePageTests(TestBaseUsersApp):
    def setUp(self) -> None:
        self.url_profile = reverse(
            'users:profile_data',
            kwargs={'username': 'something'})
        self.url_profile_update = reverse('users:profile_update')
        self.execute_register()
        return super().setUp()

    def test_profile_view_function(self):
        view = resolve(self.url_profile)
        self.assertEqual(view.func, views.profile_user_data)

    def test_profile_redirect_if_not_loged_in(self):
        response = self.client.get(self.url_profile)
        self.assertEqual(302, response.status_code)

    def test_profile_template_used(self):
        self.execute_login()
        user_data = self.generate_form_login()
        response = self.client.get(reverse(
            'users:profile_data',
            kwargs={'username': user_data['username']}))
        self.assertTemplateUsed(response, 'users/pages/profile.html')


class UsersAppProfileUpdateTests(TestBaseUsersApp):
    def setUp(self) -> None:
        self.url_profile_update = reverse('users:profile_update')
        self.profile_form_data = self.generate_form_profile()
        if self._testMethodName != ('test_profile_update'
                                    '_redirect_if_not_logged_in'):
            self.execute_register()
            self.execute_login()
        return super().setUp()

    def test_profile_update_view_function(self):
        view = resolve(self.url_profile_update)
        self.assertEqual(view.func, views.perfil_update)

    def test_profile_update_template_used(self):
        response = self.client.get(self.url_profile_update)
        self.assertTemplateUsed(response, 'users/pages/profile_update.html')

    def test_profile_update_redirect_if_not_logged_in(self):
        response = self.client.get(self.url_profile_update)
        self.assertEqual(response.status_code, 302)

    def test_profile_update_form_instance(self):
        response = self.client.get(self.url_profile_update)
        for field in self.profile_form_data:
            self.assertIn(self.profile_form_data[field],
                          response.content.decode('utf-8'))

    def test_profile_update_form_sucessful_update(self):
        self.profile_form_data['username'] = 'NovoUsername'
        response = self.client.post(
            self.url_profile_update, data=self.profile_form_data, follow=True)
        msg = 'perfil atualizado com sucesso!'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_profile_update_invalid_form(self):
        self.profile_form_data['username'] = ''
        response = self.client.post(
            self.url_profile_update, data=self.profile_form_data, follow=True)
        msg = 'opa! verifique se você preencheu corretamente os campos'
        self.assertIn(msg, response.content.decode('utf-8'))


class UsersAppChangePasswordTests(TestBaseUsersApp):
    def setUp(self) -> None:
        if self._testMethodName != ('test_change_password'
                                    '_redirect_if_not_logged_in'):
            self.execute_register()
            self.execute_login()
        self.url_change_password = reverse('users:change_password')
        self.password_form_data = self.generate_form_password()
        return super().setUp()

    def test_change_password_redirect_if_not_logged_in(self):
        response = self.client.get(self.url_change_password)
        self.assertEqual(302, response.status_code)

    def test_change_password_view_function(self):
        view = resolve(self.url_change_password)
        self.assertEqual(view.func, views.change_password)

    def test_change_password_template_used(self):
        response = self.client.get(self.url_change_password)
        self.assertTemplateUsed(response, 'users/pages/change_password.html')

    def test_change_password_invalid_form(self):
        self.password_form_data['new_password1'] = 'Password123'
        response = self.client.post(
            self.url_change_password, self.password_form_data, follow=True)
        msg = 'Erro no formulário'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_change_password_suscesfull(self):
        response = self.client.post(
            self.url_change_password, self.password_form_data, follow=True)
        msg = 'Senha alterada com sucesso!'
        self.assertIn(msg, response.content.decode('utf-8'))
