from django.urls import resolve, reverse

from learn_lab import views

from .test_learn_lab_base import LearnLabBaseTests


class LearnLabDetailViewTests(LearnLabBaseTests):
    def setUp(self) -> None:
        self.url = reverse('learn_lab:learn_lab_activity',
                           kwargs={'slug': 'activity-title'})
        return super().setUp()

    def test_learn_lab_detail_viewfunc(self):
        view = resolve(self.url)
        self.assertIs(view.func.view_class, views.LearnLabDetailView)

    def test_learn_lab_detail_raise_http_404_if_no_activity(self):
        response = self.client.get(reverse('learn_lab:learn_lab_activity',
                                   kwargs={'slug': 'something'}))
        self.assertTemplateUsed(response, "not_found.html")

    def test_learn_lab_detail_template(self):
        activity = self.activity_create()
        response = self.client.get(reverse('learn_lab:learn_lab_activity',
                                           kwargs={'slug': activity.slug}))
        self.assertTemplateUsed(
            response, 'learn_lab/pages/learn_lab_activity_detail.html')
