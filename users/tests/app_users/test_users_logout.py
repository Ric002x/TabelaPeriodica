from .test_app_users_base import TestBaseUsersApp
from django.urls import reverse


class UsersAppLogoutTests(TestBaseUsersApp):
    def setUp(self) -> None:
        if self._testMethodName != 'test_logout_redirect_if_not_logged_in':
            self.execute_register()
            self.execute_login()
        self.url_logout = reverse('users:logout')
        return super().setUp()

    def test_logout_redirect_if_not_logged_in(self):
        response = self.client.post(self.url_logout)
        self.assertEqual(302, response.status_code)

    def test_logout_raise_warning_if_not_post(self):
        response = self.client.get(self.url_logout, follow=True)
        msg = 'Logout Inválido'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_logout_raise_warning_if_not_corret_user(self):
        response = self.client.post(
            self.url_logout, data={'username': 'wronguser'}, follow=True)
        msg = 'Logout inválido'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_logout_sussessful(self):
        response = self.client.post(
            self.url_logout, data={'username': 'username'}, follow=True)
        msg = 'Usuário desconectado'
        self.assertIn(msg, response.content.decode('utf-8'))
