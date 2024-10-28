from django.core.exceptions import ValidationError

from .test_base_app_tabela import TableElementsBaseTest


class TestTabelaElementPage(TableElementsBaseTest):
    def setUp(self) -> None:
        self.element = self.make_element()
        self.element.full_clean()
        self.element.save()
        return super().setUp()

    def test_model_returns_name(self):
        self.element.name = "Teste"
        self.assertEqual(str(self.element), 'Teste')

    def test_symbol_max_lengh(self):
        self.element.symbol = 'a' * 3
        with self.assertRaises(ValidationError):
            self.element.full_clean()

    def test_atomic_number_is_integer(self):
        self.element.atomic_number = ''
        with self.assertRaises(ValidationError):
            self.element.full_clean()

        self.element.atomic_number = 3
        self.element.full_clean()
        self.assertEqual(self.element.atomic_number, 3)

    def test_get_css_class(self):
        elements_caregory = {'ametal': ['H']}
        self.element.elements_caregory = elements_caregory
        self.assertEqual(self.element.get_css_class(), 'ametal')

        self.element.name = 'Teste'
        self.element.slug = 'teste'
        self.element.symbol = 'T'
        self.element.full_clean()
        self.element.elements_caregory = elements_caregory
        self.assertEqual(self.element.get_css_class(), 'unknown')

    def test_class_methods_to_return_different_type_of_temperature(self):
        # Celcius
        self.assertEqual(self.element.melting_point, 1)
        self.assertEqual(self.element.boiling_point, 5)

        # Fahrenheit
        self.assertEqual(self.element.melting_point_fahrenheit(), 33.8)
        self.assertEqual(self.element.boiling_point_fahrenheit(), 41)

        # Kelvin
        self.assertEqual(self.element.melting_point_kelvin(), 274.15)
        self.assertEqual(self.element.boiling_point_kelvin(), 278.15)
