from django.test import TestCase
from django.urls import resolve, reverse

from periodic_table import views


class TestTablePage(TestCase):
    def test_tabela_view(self):
        view = resolve(reverse("periodic_table:table"))
        self.assertIs(view.func, views.table_list_view)

    def test_tabela_status_code_200(self):
        response = self.client.get(reverse("periodic_table:table"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_tabela_loads_correct_template(self):
        response = self.client.get(reverse("periodic_table:table"))
        self.assertTemplateUsed(response, 'periodic_table/pages/table.html')
