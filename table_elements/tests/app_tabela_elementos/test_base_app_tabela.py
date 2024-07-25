from django.test import TestCase
from table_elements.models import Elements


class ElementsMixin:
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
            year_discovered=year_discovered)
        return element


class TableElementsBaseTest(TestCase, ElementsMixin):
    def setUp(self) -> None:
        return super().setUp()
