from django.urls import resolve, reverse

from periodic_table import views

from .test_base_app_tabela import TableElementsBaseTest


class TestTableElementPage(TableElementsBaseTest):
    def setUp(self) -> None:
        self.element1 = self.make_element()
        self.element2 = self.make_element(
            name='Hélio', atomic_number=2,
        )
        self.element3 = self.make_element(
            name='Lítio', atomic_number=3,
        )

        return super().setUp()

    def test_element_view(self):
        view = resolve(reverse("periodic_table:single_element",
                               kwargs=({'slug': 'something'})))
        self.assertIs(view.func.view_class, views.ElementDetailView)

    def test_element_status_code_404_if_element_doesnt_exist(self):
        response = self.client.get(reverse("periodic_table:single_element",
                                           kwargs=({'slug': 'something'})))
        self.assertEqual(response.status_code, 404)

    def test_element_status_code_200_if_element_exist(self):
        response = self.client.get(reverse("periodic_table:single_element",
                                           kwargs=({'slug': 'hidrogenio'})))
        self.assertEqual(response.status_code, 200)

    def test_element_loads_correct_template(self):
        response = self.client.get(reverse("periodic_table:single_element",
                                           kwargs=({'slug': 'hidrogenio'})))
        self.assertTemplateUsed(
            response, 'periodic_table/pages/single_element.html')

    def test_element_detail_has_prev_and_next_elements(self):
        response = self.client.get(reverse("periodic_table:single_element",
                                           kwargs=({'slug': 'hidrogenio'})))
        self.assertEqual(response.context['next_element'], self.element2)

        response = self.client.get(reverse("periodic_table:single_element",
                                           kwargs=({'slug': 'helio'})))
        self.assertEqual(response.context['prev_element'], self.element1)

    def test_element_detail_no_next_element(self):
        response = self.client.get(reverse("periodic_table:single_element",
                                           kwargs=({'slug': 'litio'})))
        self.assertIsNone(response.context['next_element'])
        self.assertEqual(response.context['prev_element'], self.element2)

    def test_element_detail_no_prev_element(self):
        response = self.client.get(reverse("periodic_table:single_element",
                                           kwargs=({'slug': 'hidrogenio'})))
        self.assertIsNone(response.context['prev_element'])
        self.assertEqual(response.context['next_element'], self.element2)
