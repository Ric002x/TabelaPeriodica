from django.test import TestCase
from table_elements.models import Elements
from django.core.exceptions import ValidationError


class TestTabelaElementPage(TestCase):
    def setUp(self) -> None:
        self.element = self.make_element()
        return super().setUp()

    def make_element(
            self,
            name='Hidrogênio',
            slug='hidrogenio',
            symbol='H',
            atomic_number=1,
            atomic_mass=1.006,
            electrons_number=1,
            neutrons_number=0,
            density=1,
            melting_point=1,
            boiling_point=1,
            state_matter='Líquido',
            electronic_configuration="1s¹",
            ionic_states="H+",
            discoverer="someone",
            year_discovered=1900):
        element = Elements.objects.create(
            name=name,
            slug=slug,
            symbol=symbol,
            atomic_number=atomic_number,
            atomic_mass=atomic_mass,
            electrons_number=electrons_number,
            neutrons_number=neutrons_number,
            density=density,
            melting_point=melting_point,
            boiling_point=boiling_point,
            state_matter=state_matter,
            electronic_configuration=electronic_configuration,
            ionic_states=ionic_states,
            discoverer=discoverer,
            year_discovered=year_discovered,
        )
        element.full_clean()
        element.save()
        return element

    def test_model_returns_name(self):
        self.element.name = "Teste"
        self.assertEqual(str(self.element), 'Teste')

    def test_slug_max_lengh(self):
        self.element.slug = 'a' * 31
        with self.assertRaises(ValidationError):
            self.element.full_clean()

    def test_symbol_max_lengh(self):
        self.element.symbol = 'a' * 6
        with self.assertRaises(ValidationError):
            self.element.full_clean()

    def test_atomic_number_is_integer(self):
        self.element.atomic_number = ''
        with self.assertRaises(ValidationError):
            self.element.full_clean()

        self.element.atomic_number = 3
        self.element.full_clean()
        self.assertEqual(self.element.atomic_number, 3)
