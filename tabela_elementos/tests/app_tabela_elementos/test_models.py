from django.test import TestCase
from tabela_elementos.models import Elements


class TestTabelaElementPage(TestCase):
    def setUp(self) -> None:
        self.element = self.make_element()
        return super().setUp()

    def make_element(self):
        element = Elements(
            name='Hidrogen',
            slug='hidrogen',
            simbol='H',
            atomic_number=1,
            atomic_mass=1.006,
        )
        element.full_clean()
        element.save()
        return element

    def test_model_returns_name(self):
        self.element.name = 'Hidrogênio'
        self.element.full_clean()
        self.element.save()
        self.assertEqual(str(self.element), 'Hidrogênio')

    def test_return_get_absolute_url(self):
        self.element
        response = self.client.get(Elements.get_absolute_url(self.element))
        self.assertIn('Hidrogen', response.content.decode('utf-8'))
