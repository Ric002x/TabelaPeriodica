from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .test_app_users_base import UsersMixin


def url_user_api(type='list', username=None):
    if type == 'list':
        url = reverse(f'users:users-api-{type}')
    elif type == 'detail':
        url = reverse(f'users:users-api-{type}',
                      kwargs={'username': username})

    return url


def api_token_urls():
    url = reverse('users:token_obtain_pair')
    return url


class UsersAPITests(APITestCase, UsersMixin):
    def setUp(self) -> None:
        self.user_data = self.generate_form_register()
        return super().setUp()

    def test_users_get_list_return_error_404(self):
        token = self.get_login_jwt_access_token(data=self.user_data)
        response = self.client.get(
            url_user_api(),
            headers={'Authorization': f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 404)

    def test_create_user_api(self):
        # Test method POST - Creating user through API
        response = self.client.post(
            url_user_api(), data=self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def get_login_jwt_access_token(self, create_user=True, data=None):
        # Function to create an access token for logged user
        if create_user is True:
            self.create_user()
        else:
            ...
        response = self.client.post(
            api_token_urls(), data=data, format='json')
        access_token = response.data.get('access')  # type: ignore
        return access_token

    def test_logged_user_info(self):
        # Test method GET - Accessing user info with jwt token
        token = self.get_login_jwt_access_token(data=self.user_data)
        response = self.client.get(
            url_user_api('detail', 'username'),
            headers={'Authorization': f"Bearer {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Asserting if data for create user corresponds with data in response
        del self.user_data['agree_to_terms']
        del self.user_data['password']
        del self.user_data['password2']
        for key, value in self.user_data.items():
            self.assertIn(value, response.data.get(key))  # type: ignore

    def test_access_forbidden_for_user_info(self):
        # User 1 - Token:
        token_1 = self.get_login_jwt_access_token(data=self.user_data)
        # User 2:
        self.create_user(
            username='username2',
            email='teste2@email.com'
        )

        # Access Forbidden to other user infos
        response = self.client.get(
            url_user_api('detail', 'username2'),
            headers={'Authorization': f"Bearer {token_1}"}
        )
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_unauthorized_if_not_jtw_token(self):
        self.create_user()
        response = self.client.get(
            url_user_api('detail', 'username')
        )
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )

    def test_user_update_return_200_if_no_data(self):
        user = self.create_user()
        token_1 = self.get_login_jwt_access_token(False, data={
            "username": user.username,
            "password": "Password123"
        })

        response = self.client.patch(
            url_user_api('detail', user.username),
            headers={'Authorization': f"Bearer {token_1}"}
        )
        self.assertEqual(response.status_code, 200)

    def test_user_update_validations_errors(self):
        user = self.create_user()
        token_1 = self.get_login_jwt_access_token(False, data={
            "username": user.username,
            "password": "Password123"
        })
        self.user_data = self.generate_form_profile()
        del self.user_data['username']
        for key, value in self.user_data.items():
            response = self.client.patch(
                url_user_api('detail', user.username),
                data={key: ""},
                headers={'Authorization': f"Bearer {token_1}"}
            )
            self.assertIn("Esse campo é obrigatório",
                          response.content.decode('utf-8'))
        response = self.client.patch(
            url_user_api('detail', user.username),
            data={'username': ""},
            headers={'Authorization': f"Bearer {token_1}"}
        )
        self.assertIn("Este campo não pode ser em branco",
                      response.content.decode('utf-8'))

    def test_user_update_cant_update_password(self):
        user = self.create_user()
        token_1 = self.get_login_jwt_access_token(False, data={
            "username": user.username,
            "password": "Password123"
        })
        response = self.client.patch(
            url_user_api('detail', user.username),
            data={'password': "password123"},
            headers={'Authorization': f"Bearer {token_1}"}
        )
        msg = "Não é possível atualizar a senha nesta url"
        self.assertIn(msg, response.content.decode('utf-8'))


class UserAPIChangePasswordTests(APITestCase, UsersMixin):
    def setUp(self) -> None:
        self.token = self.get_login_jwt_access_token(data={
            "username": "username",
            "password": "Password123"
        })
        return super().setUp()

    def get_login_jwt_access_token(self, create_user=True, data=None):
        # Function to create an access token for logged user
        if create_user is True:
            self.create_user()
        else:
            ...
        response = self.client.post(
            api_token_urls(), data=data, format='json')
        access_token = response.data.get('access')  # type: ignore
        return access_token

    def get_url(self, username):
        url = reverse("users:change_password_api",
                      kwargs={'username': username})
        return url

    def test_change_password_requires_token(self):
        response = self.client.patch(self.get_url('username'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_password_user_not_found(self):
        response = self.client.patch(
            self.get_url('another_user'), headers={
                'Authorization': f"Bearer {self.token}"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_change_password_user_cant_update_other_user_password(self):
        self.create_user(
            username="another_user", email="anotheruser@email.com")
        response = self.client.patch(
            self.get_url('another_user'), headers={
                'Authorization': f"Bearer {self.token}"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_change_password_form_validation_old_password(self):
        response = self.client.patch(
            self.get_url('username'), headers={
                'Authorization': f"Bearer {self.token}"})
        msg = "Campo obrigatório"
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response2 = self.client.patch(
            self.get_url('username'), headers={
                'Authorization': f"Bearer {self.token}"},
            data={'old_password': "different_password"})
        msg = "A senha antiga está incorreta."
        self.assertIn(msg, response2.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_successful_save(self):
        data = {
            'old_password': "Password123",
            "new_password": "NewPassword1",
            "repeat_password": "NewPassword1"
        }
        response = self.client.patch(
            self.get_url('username'),
            headers={'Authorization': f"Bearer {self.token}"},
            data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
