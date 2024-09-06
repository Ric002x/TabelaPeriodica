from django.test import TestCase
from django.urls import resolve, reverse

from periodic_table import views


class TestPoliciesPage(TestCase):
    def setUp(self) -> None:
        self.url = reverse('periodic_table:privacy_police')
        return super().setUp()

    def test_policies_view_function(self):
        view = resolve(self.url)
        self.assertEqual(view.func, views.privacy_police_view)

    def test_policies_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response, 'periodic_table/pages/privacy_police.html')
