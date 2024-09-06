from .test_base_app_tabela import TableElementsBaseTest
from django.core.exceptions import ValidationError


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
