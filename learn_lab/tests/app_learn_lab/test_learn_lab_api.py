from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.test import APITestCase

from learn_lab.models import Activity

from .test_learn_lab_base import ActivityMixin


def url_list(page=None):
    if not page:
        url_list = reverse('learn_lab:activity-api-list')
    else:
        url_list = reverse(
            'learn_lab:activity-api-list') + f'?page={page}'
    return url_list


def api_token_urls():
    url = reverse('users:token_obtain_pair')
    return url


class ActivityAPIGetListTests(APITestCase, ActivityMixin):
    def test_view_function(self):
        view = resolve(url_list())
        self.assertIn('ActivityViewSet', str(view.func))

    def test_http_get_list_status_200(self):
        self.activity = self.activity_create()
        response = self.client.get(url_list())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_itens_per_page_pagination_for_activity(self):
        self.subject1 = self.create_subject()
        self.level1 = self.create_level()

        self.bulk_create_activity(
            range(1, 31), subject=self.subject1, level=self.level1)
        response = self.client.get(url_list())
        results = len(response.data['results'])  # type: ignore
        self.assertEqual(results, 20)

        response2 = self.client.get(url_list(2))
        results = len(response2.data['results'])  # type: ignore
        self.assertEqual(results, 10)

    def test_get_only_published_activities(self):
        self.subject1 = self.create_subject()
        self.level1 = self.create_level()

        self.bulk_create_activity(
            range(1, 11), subject=self.subject1, level=self.level1)

        self.activity_create(is_published=False)
        response = self.client.get(url_list())
        results = len(response.data['results'])  # type: ignore
        self.assertEqual(results, 10)


class ActivityAPIsAuthorizationTests(APITestCase, ActivityMixin):
    def setUp(self) -> None:
        self.user = self.create_user()
        user_data = {'username': 'username', 'password': 'Password123'}

        self.token = self.get_login_jwt_access_token(False, user_data)

        self.user2 = self.create_user(
            username='username2',
            email='teste2@email.com'
        )

        self.data = self.generate_form_activity()
        del self.data['file']
        self.data['subject'] = 1
        self.data['level'] = 1

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

    def test_client_cannot_create_activity_without_send_jwt(self):
        response = self.client.post(url_list(), data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_activity_with_logged_user(self):
        response = self.client.post(
            url_list(), self.data, format='json',
            headers={'Authorization': f"Bearer {self.token}"})
        self.assertEqual(response.data['user']['id'], 1)  # type: ignore
        self.assertEqual(
            response.data['user']['username'], "username")  # type: ignore
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_activity_owner_can_patch(self):
        activity = Activity.objects.create(
            title='Test',
            user=self.user,
            is_published=True
        )
        response = self.client.patch(
            reverse('learn_lab:activity-api-detail',
                    kwargs={'slug': activity.slug}), self.data, format="json",
            headers={'Authorization': f"Bearer {self.token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activity_not_owner_cannot_patch(self):
        activity = self.activity_create(
            simple=True,
            id=2)
        response = self.client.patch(
            reverse('learn_lab:activity-api-detail',
                    kwargs={'slug': activity.slug}), self.data, format="json",
            headers={'Authorization': f"Bearer {self.token}"})
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN)


def url_list_foreignkeys(foreignkey='subject', id=1):
    url = reverse(f'learn_lab:activity-api-{foreignkey}',
                  kwargs={'pk': id})
    return url


class ActivityListSubjectAndLevelTests(APITestCase, ActivityMixin):
    def setUp(self) -> None:
        self.subject1 = self.create_subject()
        self.subject2 = self.create_subject(name="Matemática")
        self.level1 = self.create_level(name="8º ano EF")
        self.level2 = self.create_level()

        self.bulk_create_activity(
            range(1, 11), subject=self.subject1, level=self.level1)
        self.bulk_create_activity(
            range(11, 21), subject=self.subject2, create_user=False,
            level=self.level2)

        return super().setUp()

    def test_get_subject_list_status_200(self):
        response = self.client.get(url_list_foreignkeys())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # type: ignore

    def test_get_subject_for_id(self):
        response = self.client.get(url_list_foreignkeys())
        results = response.data['results']   # type: ignore
        for item in results:
            subject1 = item['subject']
            self.assertEqual(subject1['id'], 1)
            self.assertEqual(subject1['name'], 'Ciências')

        response2 = self.client.get(url_list_foreignkeys(id=2))
        results2 = response2.data['results']   # type: ignore
        for item in results2:
            subject2 = item['subject']
            self.assertEqual(subject2['id'], 2)
            self.assertEqual(subject2['name'], 'Matemática')

    def test_get_level_list_status_200(self):
        response = self.client.get(url_list_foreignkeys('level'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # type: ignore

    def test_get_level_for_id(self):
        response = self.client.get(url_list_foreignkeys('level'))
        results = response.data['results']  # type: ignore
        for item in results:
            level1 = item['level']
            self.assertEqual(level1['id'], 1)
            self.assertEqual(level1['name'], "8º ano EF")

        response2 = self.client.get(url_list_foreignkeys('level', id=2))
        results2 = response2.data['results']  # type: ignore
        for item in results2:
            level2 = item['level']
            self.assertEqual(level2['id'], 2)
            self.assertEqual(level2['name'], '9º ano EF')
