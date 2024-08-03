from django.test import TestCase
from django.urls import reverse, resolve
from table_elements import views


class TestTabelaMainPage(TestCase):
    def test_main_page_view(self):
        view = resolve(reverse("table_elements:home"))
        self.assertIs(view.func, views.home_page_view)

    def test_main_page_status_code_200(self):
        response = self.client.get(reverse("table_elements:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_main_page_loads_correct_template(self):
        response = self.client.get(reverse("table_elements:home"))
        self.assertTemplateUsed(response, 'table_elements/pages/main_page.html')
