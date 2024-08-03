from .test_learn_lab_base import LearnLabBaseTests
from django.urls import reverse, resolve
from learn_lab import views


class LearnLabListViewTests(LearnLabBaseTests):
    def setUp(self) -> None:
        self.activity = self.activity_create()
        self.url = reverse('learn_lab:learn_lab_home')
        return super().setUp()

    def test_learn_lab_list_view_function(self):
        view = resolve(self.url)
        self.assertIs(view.func, views.lear_lab_list_view)

    def test_learn_lab_list_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'learn_lab/pages/learn_lab_home.html')

    def test_learn_lab_list_view_search_page(self):
        response = self.client.get(
            reverse('learn_lab:learn_lab_activity_search') + '?q=a')
        self.assertIsNotNone(response.context['search_term'])
        self.assertIsNotNone(response.context['learn_lab_search_page'])
