from django.test import TestCase
from django.urls import reverse, resolve
from table_elements import views
from table_elements.models import Elements


def create_element():
    element = Elements.objects.create(
        name='Hidrogênio',
        slug='hidrogenio',
        symbol='H',
        atomic_number=1,
        atomic_mass=1.006,
        electrons_number=1,
        neutrons_number="0",
        density=1,
        melting_point=1,
        boiling_point=1,
        state_matter='Líquido',
        electronic_configuration="1s¹",
        ionic_states="H+",
        discoverer="someone",
        year_discovered=1900,
    )
    element.save()


class TestTabelaElementPage(TestCase):
    def test_element_view(self):
        view = resolve(reverse("table_elements:single_element",
                               kwargs=({'slug': 'something'})))
        self.assertIs(view.func.view_class, views.ElementsDetailView)

    def test_element_status_code_404_if_element_doesnt_exist(self):
        response = self.client.get(reverse("table_elements:single_element",
                                           kwargs=({'slug': 'something'})))
        self.assertEqual(response.status_code, 404)

    def test_element_status_code_200_if_element_exist(self):
        create_element()
        response = self.client.get(reverse("table_elements:single_element",
                                           kwargs=({'slug': 'hidrogenio'})))
        self.assertEqual(response.status_code, 200)

    def test_recipe_element_loads_correct_template(self):
        create_element()
        response = self.client.get(reverse("table_elements:single_element",
                                           kwargs=({'slug': 'hidrogenio'})))
        self.assertTemplateUsed(
            response, 'partials/element_detail/hidrogenio.html')
