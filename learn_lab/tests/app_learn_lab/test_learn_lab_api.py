from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from learn_lab.models import Activity

from .test_learn_lab_base import ActivityMixin


def url_list(page=None):
    if not page:
        url_list = reverse('learn_lab:activity-api-v2-list')
    else:
        url_list = reverse(
            'learn_lab:activity-api-v2-list') + f'?page={page}'
    return url_list


class ActivityAPIsTests(APITestCase, ActivityMixin):
    def test_view_function(self):
        view = resolve(url_list())
        self.assertIn('ActivityViewSet', str(view.func))

    def test_http_get_list_status_200(self):
        self.activity = self.activity_create()
        response = self.client.get(url_list())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_itens_per_page_pagination_for_activity(self):
        self.bulk_create_activity(range(30))
        response = self.client.get(url_list())
        results = len(response.data['results'])  # type: ignore
        self.assertEqual(results, 20)

        response2 = self.client.get(url_list(2))
        results = len(response2.data['results'])  # type: ignore
        self.assertEqual(results, 10)

    def test_get_only_published_activities(self):
        self.bulk_create_activity(range(10))
        self.activity_create(is_published=False)
        response = self.client.get(url_list())
        results = len(response.data['results'])  # type: ignore
        self.assertEqual(results, 10)


class ActivityAPIsAuthorizationTests(APITestCase, ActivityMixin):
    def setUp(self) -> None:
        self.user = self.create_user()

        refresh = RefreshToken.for_user(user=self.user)
        self.access = str(refresh.access_token)  # type: ignore

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)

        self.user2 = self.create_user(
            username='username2',
            email='teste2@email.com'
        )
        self.client_not_owner = APIClient()
        self.client_not_owner.force_authenticate(user=self.user2)

        self.data = self.generate_form_activity()
        del self.data['file']
        self.data['subject'] = 1
        self.data['level'] = 1

        return super().setUp()

    def test_create_activity_with_logged_user(self):
        response = self.client.post(url_list(), self.data, format='json')
        self.assertEqual(response.data['user'], 1)  # type: ignore
        self.assertEqual(
            response.data['user_name'], "username")  # type: ignore

    def test_activity_owner_can_patch(self):
        activity = Activity.objects.create(
            title='Test',
            user=self.user,
            is_published=True
        )
        response = self.client.patch(
            reverse('learn_lab:activity-api-v2-detail',
                    kwargs={'slug': activity.slug}), self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activity_not_owner_cannot_patch(self):
        activity = self.activity_create(
            simple=True,
            user_data=self.user)
        response = self.client_not_owner.patch(
            reverse('learn_lab:activity-api-v2-detail',
                    kwargs={'slug': activity.slug}), self.data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN)  # type: ignore


def url_list_foreignkeys(foreignkey='subject', id=1):
    url = reverse(f'learn_lab:activity-api-v2-{foreignkey}',
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
            self.assertEqual(subject1, 1)
            subject_name = item['subject_name']
            self.assertEqual(subject_name, 'Ciências')

        response2 = self.client.get(url_list_foreignkeys(id=2))
        results2 = response2.data['results']   # type: ignore
        for item in results2:
            subject2 = item['subject']
            self.assertEqual(subject2, 2)
            subject_name = item['subject_name']
            self.assertEqual(subject_name, 'Matemática')

    def test_get_level_list_status_200(self):
        response = self.client.get(url_list_foreignkeys('level'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # type: ignore

    def test_get_level_for_id(self):
        response = self.client.get(url_list_foreignkeys('level'))
        results = response.data['results']  # type: ignore
        for item in results:
            level1 = item['level']
            self.assertEqual(level1, 1)
            self.assertEqual(item['level_name'], "8º ano EF")

        response2 = self.client.get(url_list_foreignkeys('level', id=2))
        results2 = response2.data['results']  # type: ignore
        for item in results2:
            level2 = item['level']
            self.assertEqual(level2, 2)
            self.assertEqual(item['level_name'], '9º ano EF')
