from .test_learn_lab_base import LearnLabBaseTests
from django.urls import reverse, resolve
from learn_lab import views


class LearnLabLevelViewTests(LearnLabBaseTests):
    def setUp(self) -> None:
        self.activity = self.activity_create()
        self.url = reverse('learn_lab:learn_lab_level',
                           kwargs={'id': self.activity.level_id})
        return super().setUp()

    def test_learn_lab_level_view_function(self):
        view = resolve(self.url)
        self.assertEqual(view.func, views.learn_lab_level_list_view)

    def test_learn_lab_level_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'learn_lab/pages/learn_lab_home.html')

    def test_learn_lab_level_raise_404_if_no_activity(self):
        response = self.client.get(reverse(
            'learn_lab:learn_lab_level', kwargs={'id': 5}))
        self.assertEqual(404, response.status_code)

    def test_learn_lab_level_has_context(self):
        response = self.client.get(self.url)
        self.assertIsNotNone(response.context['activity'].level_id)
        self.assertTrue(response.context['learn_lab_page'])
