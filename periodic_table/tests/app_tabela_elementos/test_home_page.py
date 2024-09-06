from django.test import TestCase
from django.urls import resolve, reverse

from periodic_table import views


class TestTabelaMainPage(TestCase):
    def test_main_page_view(self):
        view = resolve(reverse("periodic_table:home"))
        self.assertIs(view.func, views.home_page_view)

    def test_main_page_status_code_200(self):
        response = self.client.get(reverse("periodic_table:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_main_page_loads_correct_template(self):
        response = self.client.get(reverse("periodic_table:home"))
        self.assertTemplateUsed(
            response, 'periodic_table/pages/main_page.html')
