from django.urls import resolve, reverse

from learn_lab import views

from .test_learn_lab_base import LearnLabBaseTests


class LearnLabSubjectViewTests(LearnLabBaseTests):
    def setUp(self) -> None:
        self.activity = self.activity_create()
        subject = self.activity.subject.name
        self.url = reverse('learn_lab:learn_lab_subject',
                           kwargs={'subject': subject})
        return super().setUp()

    def test_learn_lab_subject_view_function(self):
        view = resolve(self.url)
        self.assertEqual(view.func.view_class, views.LearnLabSubjectListView)

    def test_learn_lab_subject_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response, 'learn_lab/pages/learn_lab_home.html')

    def test_learn_lab_subject_raise_404_if_no_activity(self):
        response = self.client.get(reverse(
            'learn_lab:learn_lab_subject', kwargs={'subject': 'not_subject'}))
        self.assertTemplateUsed(response, "not_found.html")

    def test_learn_lab_subject_has_context(self):
        response = self.client.get(self.url)
        self.assertIsNotNone(response.context['activity'].subject_id)
        self.assertTrue(response.context['learn_lab_page'])
