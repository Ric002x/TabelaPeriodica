from django.test import TestCase
from django.urls import reverse, resolve
from table_elements import views


class TestTablePage(TestCase):
    def test_tabela_view(self):
        view = resolve(reverse("table_elements:table"))
        self.assertIs(view.func, views.table_list_view)

    def test_tabela_status_code_200(self):
        response = self.client.get(reverse("table_elements:table"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_tabela_loads_correct_template(self):
        response = self.client.get(reverse("table_elements:table"))
        self.assertTemplateUsed(response, 'table_elements/pages/table.html')
