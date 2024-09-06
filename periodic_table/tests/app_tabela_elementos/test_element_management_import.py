from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from periodic_table.models import Element


class ImportElementTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_import_elements_command(self):
        out = StringIO()

        call_command('import_elements', stdout=out)

        output = out.getvalue()

        self.assertIn('Successfully imported elements from CSV', output)
        self.assertTrue(Element.objects.exists())
        element = Element.objects.first()
        self.assertEqual(element.atomic_number, 1)
