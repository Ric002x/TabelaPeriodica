from django.test import TestCase
from django.urls import reverse, resolve
from tabela_elementos import views


class TestTabelaMainPage(TestCase):
    def test_main_page_view(self):
        view = resolve(reverse("tabela_elementos:home"))
        self.assertIs(view.func, views.home)

    def test_main_page_status_code_200(self):
        response = self.client.get(reverse("tabela_elementos:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_main_page_loads_correct_template(self):
        response = self.client.get(reverse("tabela_elementos:home"))
        self.assertTemplateUsed(response, 'pages/main_page.html')
