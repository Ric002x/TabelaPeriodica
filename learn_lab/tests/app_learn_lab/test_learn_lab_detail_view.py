from .test_learn_lab_base import LearnLabBaseTests
from django.urls import reverse, resolve
from learn_lab import views


class LearnLabDetailViewTests(LearnLabBaseTests):
    def setUp(self) -> None:
        self.url = reverse('learn_lab:learn_lab_activity',
                           kwargs={'slug': 'activity-title'})
        return super().setUp()

    def test_learn_lab_detail_viewfunc(self):
        view = resolve(self.url)
        self.assertIs(view.func, views.learn_lab_detail_view)

    def test_learn_lab_detail_raise_http_404_if_no_activity(self):
        response = self.client.get(reverse('learn_lab:learn_lab_activity',
                                   kwargs={'slug': 'something'}))
        self.assertEqual(response.status_code, 404)

    def test_learn_lab_detail_template(self):
        activity = self.activity_create()
        response = self.client.get(reverse('learn_lab:learn_lab_activity',
                                           kwargs={'slug': activity.slug}))
        self.assertTemplateUsed(
            response, 'learn_lab/pages/learn_lab_activity_detail.html')
