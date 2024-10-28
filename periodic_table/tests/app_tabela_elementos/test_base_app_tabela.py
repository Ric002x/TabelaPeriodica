from django.template.defaultfilters import slugify
from django.test import TestCase

from periodic_table.models import Element


class ElementsMixin:
    def make_element(
        self,
        name='Hidrogênio',
        symbol='H',
        description='element sdescription',
        atomic_number=1,
        atomic_mass=1.006,
        electrons_number=1,
        neutrons_number=0,
        density=1,
        melting_point=1,
        boiling_point=5,
        state_matter='Líquido',
        electronic_configuration="1s¹",
        electron_distribution='K1 L0...',
        ionic_states="H+",
        history_and_discovery='Descovery in...',
        chemical_properties='chemical properties',
        usage='usage',
        extra_information='extra_information',
    ):
        element = Element.objects.create(
            name=name,
            slug=slugify(name),
            symbol=symbol,
            description=description,
            atomic_number=atomic_number,
            atomic_mass=atomic_mass,
            electrons_number=electrons_number,
            neutrons_number=neutrons_number,
            density=density,
            melting_point=melting_point,
            boiling_point=boiling_point,
            state_matter=state_matter,
            electronic_configuration=electronic_configuration,
            electron_distribution=electron_distribution,
            ionic_states=ionic_states,
            history_and_discovery=history_and_discovery,
            chemical_properties=chemical_properties,
            usage=usage,
            extra_information=extra_information,
        )
        return element


class TableElementsBaseTest(TestCase, ElementsMixin):
    def setUp(self) -> None:
        return super().setUp()
