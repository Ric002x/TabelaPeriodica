from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.test import APITestCase

from periodic_table.models import Element

from .test_base_app_tabela import ElementsMixin


class ElementsAPIGETList(APITestCase, ElementsMixin):
    def setUp(self) -> None:
        self.url = reverse("periodic_table:api_elements_list_view")
        return super().setUp()

    def test_view_function(self):
        view = resolve(self.url)
        self.assertIn("ElementListViewAPI", str(view.func.cls))

    def test_element_list_returns_status_200(self):
        self.make_element()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_element_list_pagination_20_items_per_page(self):
        for i in range(1, 51):
            self.make_element(atomic_number=i, name=f"element-{i}")
        response = self.client.get(self.url)
        self.assertEqual(len(response.data['results']), 20)
        self.assertEqual(response.data['results'][0]['atomic_number'], 1)

        response2 = self.client.get(self.url + '?page=2')
        self.assertEqual(len(response2.data['results']), 20)
        self.assertEqual(response2.data['results'][0]['atomic_number'], 21)


class ElementsAPIGETDetail(APITestCase, ElementsMixin):
    def setUp(self) -> None:
        self.url = reverse(
            "periodic_table:api_elements_detail_view",
            kwargs={'symbol': 'H'})
        return super().setUp()

    def test_element_detail_view_function(self):
        view = resolve(self.url)
        self.assertIn("ElementDetailViewAPI", str(view.func.cls))

    def test_element_detail_returns_status_200_if_element(self):
        self.make_element()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_element_detail_returns_status_404_if_element_not_found(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_element_detail_shows_element_temperatures_as_dict(self):
        self.make_element()
        response = self.client.get(self.url)
        melting_point_data = response.data[
            "physical_properties"]['melting_point']

        self.assertIn("Celsius", melting_point_data)
        self.assertIn("Fahrenheit", melting_point_data)
        self.assertIn("Kelvin", melting_point_data)
