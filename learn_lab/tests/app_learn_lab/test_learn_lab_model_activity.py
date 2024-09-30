from django.urls import reverse

from .test_learn_lab_base import LearnLabBaseTests


class LearnLabModelsTests(LearnLabBaseTests):
    def setUp(self) -> None:
        self.activity = self.activity_create()
        return super().setUp()

    def test_subject_str(self):
        self.activity.subject.name = "Testsujbect"
        self.assertEqual('Testsujbect', str(self.activity.subject))

    def test_level_str(self):
        self.activity.level.name = "Testlevel"
        self.assertEqual('Testlevel', str(self.activity.level))

    def test_activity_str(self):
        self.activity.title = "TestActivity"
        self.assertEqual('TestActivity', str(self.activity))

    def test_activity_get_url(self):
        expected_url = reverse('learn_lab:learn_lab_activity',
                               kwargs={'slug': self.activity.slug})
        self.assertEqual(self.activity.get_absolute_url(), expected_url)
