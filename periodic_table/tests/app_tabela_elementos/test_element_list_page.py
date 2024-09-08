from django.test import RequestFactory
from django.urls import reverse

from .test_base_app_tabela import TableElementsBaseTest


class ElementListViewTest(TableElementsBaseTest):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.url_list = reverse('periodic_table:elements_list')
        self.url_search = reverse('periodic_table:search_element')
        return super().setUp()

    def test_list_view_status_code_200_if_elements(self):
        self.make_element()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 200)

    def test_list_view_if_no_elements(self):
        response = self.client.get(self.url_list)
        msg = "Nenhum elemento encontrado"
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_list_view_template(self):
        self.make_element()
        response = self.client.get(self.url_list)
        self.assertTemplateUsed(
            response, 'periodic_table/pages/elements_list.html')

    def test_list_view_search_page_find_element(self):
        self.make_element()
        response = self.client.get(self.url_search + '?q=Hidrogênio')
        self.assertIn('Hidrogênio', response.content.decode('utf-8'))

    def test_list_view_contexts(self):
        self.make_element()
        response = self.client.get(self.url_search + '?q=Hidrogênio')
        self.assertIn('page_obj', response.context)
        self.assertEqual(response.context['page_obj'].number, 1)
        self.assertEqual(response.context['page_obj'].paginator.num_pages, 1)
        self.assertIn('element_page_search', response.context)
        self.assertTrue(response.context['element_page_search'])
