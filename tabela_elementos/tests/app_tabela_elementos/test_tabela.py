from django.test import TestCase
from django.urls import reverse, resolve
from tabela_elementos import views


class TestTabelaMainPage(TestCase):
    def test_tabela_view(self):
        view = resolve(reverse("tabela_elementos:tabela"))
        self.assertIs(view.func, views.tabela_view)

    def test_tabela_status_code_200(self):
        response = self.client.get(reverse("tabela_elementos:tabela"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_tabela_loads_correct_template(self):
        response = self.client.get(reverse("tabela_elementos:tabela"))
        self.assertTemplateUsed(response, 'pages/tabela.html')
