from django.test import TestCase
from django.core.management import call_command
from io import StringIO
from table_elements.models import Elements


class ImportElementTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_import_elements_command(self):
        out = StringIO()

        call_command('import_elements', stdout=out)

        output = out.getvalue()

        self.assertIn('Successfully imported elements from CSV', output)
        self.assertTrue(Elements.objects.exists())
        element = Elements.objects.first()
        self.assertEqual(element.atomic_number, 1)
