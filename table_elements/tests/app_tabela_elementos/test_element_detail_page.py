from django.urls import reverse, resolve
from table_elements import views
from .test_base_app_tabela import TableElementsBaseTest
from table_elements.models import Elements


class TestTableElementPage(TableElementsBaseTest):
    def setUp(self) -> None:
        self.element1 = self.make_element()
        self.element2 = self.make_element(
            name='Hélio', slug='helio', atomic_number=2,
        )
        self.element3 = self.make_element(
            name='Lítio', slug='litio', atomic_number=3,
        )

        return super().setUp()

    def test_element_view(self):
        view = resolve(reverse("table_elements:single_element",
                               kwargs=({'slug': 'something'})))
        self.assertIs(view.func, views.element_detail_view)

    def test_element_status_code_404_if_element_doesnt_exist(self):
        response = self.client.get(reverse("table_elements:single_element",
                                           kwargs=({'slug': 'something'})))
        self.assertEqual(response.status_code, 404)

    def test_element_status_code_200_if_element_exist(self):
        response = self.client.get(reverse("table_elements:single_element",
                                           kwargs=({'slug': 'hidrogenio'})))
        self.assertEqual(response.status_code, 200)

    def test_element_loads_correct_template(self):
        response = self.client.get(reverse("table_elements:single_element",
                                           kwargs=({'slug': 'hidrogenio'})))
        self.assertTemplateUsed(
            response, 'partials/element_detail/hidrogenio.html')

    def test_element_detail_has_prev_and_next_elements(self):
        response = self.client.get(reverse("table_elements:single_element",
                                           kwargs=({'slug': 'hidrogenio'})))
        self.assertEqual(response.context['next_element'], self.element2)

        response = self.client.get(reverse("table_elements:single_element",
                                           kwargs=({'slug': 'helio'})))
        self.assertEqual(response.context['prev_element'], self.element1)

    def test_element_detail_prev_and_next_elements_is_none(self):
        Elements.objects.all().delete()
        self.make_element()

        response = self.client.get(reverse('table_elements:single_element',
                                           kwargs={'slug': 'hidrogenio'}))
        self.assertIsNone(response.context['prev_element'])
        self.assertIsNone(response.context['next_element'])

    def test_element_detail_no_next_element(self):
        response = self.client.get(reverse("table_elements:single_element",
                                           kwargs=({'slug': 'litio'})))
        self.assertIsNone(response.context['next_element'])
        self.assertEqual(response.context['prev_element'], self.element2)

    def test_element_detail_no_prev_element(self):
        response = self.client.get(reverse("table_elements:single_element",
                                           kwargs=({'slug': 'hidrogenio'})))
        self.assertIsNone(response.context['prev_element'])
        self.assertEqual(response.context['next_element'], self.element2)
