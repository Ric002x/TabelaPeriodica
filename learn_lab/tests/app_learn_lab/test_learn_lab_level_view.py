from django.urls import resolve, reverse

from learn_lab import views

from .test_learn_lab_base import LearnLabBaseTests


class LearnLabLevelViewTests(LearnLabBaseTests):
    def setUp(self) -> None:
        self.activity = self.activity_create()
        level = self.activity.level.name
        self.url = reverse('learn_lab:learn_lab_level',
                           kwargs={'level': level})
        return super().setUp()

    def test_learn_lab_level_view_function(self):
        view = resolve(self.url)
        self.assertEqual(view.func.view_class, views.LearnLabLevelListView)

    def test_learn_lab_level_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response, 'learn_lab/pages/learn_lab_home.html')

    def test_learn_lab_level_raise_404_if_no_activity(self):
        response = self.client.get(reverse(
            'learn_lab:learn_lab_level', kwargs={'level': 'not_level'}))
        self.assertTemplateUsed(response, "not_found.html")

    def test_learn_lab_level_has_context(self):
        response = self.client.get(self.url)
        self.assertTrue(response.context['learn_lab_page'])
