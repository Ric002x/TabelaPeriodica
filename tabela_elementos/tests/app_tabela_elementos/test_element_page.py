from django.test import TestCase
from django.urls import reverse, resolve
from tabela_elementos import views
from tabela_elementos.models import Elements


class TestTabelaElementPage(TestCase):
    def test_element_view(self):
        view = resolve(reverse("tabela_elementos:single_element",
                               kwargs=({'slug': 'something'})))
        self.assertIs(view.func, views.single_element_view)

    def test_element_status_code_404_if_element_doesnt_exist(self):
        response = self.client.get(reverse("tabela_elementos:single_element",
                                           kwargs=({'slug': 'something'})))
        self.assertEqual(response.status_code, 404)

    def test_element_status_code_200_if_element_exist(self):
        Elements.objects.create(
            name='Hidrogen',
            slug='hidrogen',
            simbol='H',
            atomic_number=1,
            atomic_mass=1.006,
        )
        response = self.client.get(reverse("tabela_elementos:single_element",
                                           kwargs=({'slug': 'hidrogen'})))
        self.assertEqual(response.status_code, 200)

    def test_recipe_element_loads_correct_template(self):
        Elements.objects.create(
            name='Hidrogen',
            slug='hidrogen',
            simbol='H',
            atomic_number=1,
            atomic_mass=1.006,
        )
        response = self.client.get(reverse("tabela_elementos:single_element",
                                           kwargs=({'slug': 'hidrogen'})))
        self.assertTemplateUsed(response, 'pages/single_element.html')
