from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .test_app_users_base import UsersMixin


def url_user_api(method='list', username=None):
    if method == 'list':
        url = reverse(f'users:users-api-v2-{method}')
    elif method == 'detail':
        url = reverse(f'users:users-api-v2-{method}',
                      kwargs={'username': username})
    return url


def api_token_urls():
    url = reverse('learn_lab:token_obtain_pair')
    return url


class UsersAPITests(APITestCase, UsersMixin):
    def setUp(self) -> None:
        self.user_data = self.generate_form_register()
        return super().setUp()

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

        # Asserting if data for create user corresponds with data in reponse
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
