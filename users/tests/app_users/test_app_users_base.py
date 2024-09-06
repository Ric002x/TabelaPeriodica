from django.test import TestCase
from django.urls import reverse


class UsersMixin:
    def generate_form_register(self):
        register_form_data = {
            'first_name': 'User',
            'last_name': 'Name',
            'username': 'username',
            'password': 'Password123',
            'password2': 'Password123',
            'email': 'teste@email.com',
            'agree_to_terms': True,
        }
        return register_form_data

    def generate_form_login(self):
        login_form_data = {
            'username': 'username',
            'password': 'Password123',
        }
        return login_form_data

    def generate_form_profile(self):
        profile_form_data = {
            'first_name': 'User',
            'last_name': 'Name',
            'username': 'username',
            'email': 'teste@email.com',
        }
        return profile_form_data

    def generate_form_password(self):
        password_form_data = {
            'old_password': 'Password123',
            'new_password1': 'NewPassoword123',
            'new_password2': 'NewPassoword123',
        }
        return password_form_data

    def execute_register(self):
        self.client.post(reverse(  # type: ignore
            'users:register_create'), data=self.generate_form_register())

    def execute_login(self):
        self.client.post(reverse(  # type: ignore
            'users:login_create'), data=self.generate_form_login())


class TestBaseUsersApp(TestCase, UsersMixin):
    def setUp(self) -> None:
        return super().setUp()
