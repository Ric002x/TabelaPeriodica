from .test_learn_lab_base import LearnLabBaseTests
from django.urls import reverse


class RatingCrudTests(LearnLabBaseTests):
    def setUp(self) -> None:
        self.activity = self.activity_create()
        self.execute_login()
        self.rating_form_data = self.generate_form_rating()
        return super().setUp()

    def test_rating_create(self):
        response = self.client.post(
            reverse('learn_lab:activity_rate_create',
                    kwargs={'slug': self.activity.slug}),
            data=self.rating_form_data, follow=True,)
        msg = 'Avalição enviada'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_rating_create_invalid_form(self):
        self.rating_form_data['rating'] = 'string'
        response = self.client.post(
            reverse('learn_lab:activity_rate_create',
                    kwargs={'slug': self.activity.slug}),
            data=self.rating_form_data, follow=True,)
        msg = 'Erro na avaliação'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_rating_comment_empty_sucess(self):
        self.rating_form_data['comment'] = ''
        response = self.client.post(
            reverse('learn_lab:activity_rate_create',
                    kwargs={'slug': self.activity.slug}),
            data=self.rating_form_data, follow=True,)
        msg = 'Avalição enviada'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_rating_update(self):
        self.client.post(
            reverse('learn_lab:activity_rate_create',
                    kwargs={'slug': self.activity.slug}),
            data=self.rating_form_data, follow=True)

        response = self.client.post(
            reverse('learn_lab:activity_rate_edit',
                    kwargs={'slug': self.activity.slug}),
            data=self.rating_form_data, follow=True
        )
        msg = 'Sua avalição foi alterada!'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_rating_update_invalid(self):
        self.client.post(
            reverse('learn_lab:activity_rate_create',
                    kwargs={'slug': self.activity.slug}),
            data=self.rating_form_data, follow=True)

        self.rating_form_data['rating'] = 'string'
        response = self.client.post(
            reverse('learn_lab:activity_rate_edit',
                    kwargs={'slug': self.activity.slug}),
            data=self.rating_form_data, follow=True
        )
        msg = 'Erro no formulário'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_rating_delete(self):
        self.client.post(
            reverse('learn_lab:activity_rate_create',
                    kwargs={'slug': self.activity.slug}),
            data=self.rating_form_data, follow=True)

        response = self.client.post(
            reverse('learn_lab:activity_rate_delete',
                    kwargs={'slug': self.activity.slug}),
            follow=True
        )
        msg = 'Avalição deletada'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_rating_raise_404_if_get(self):
        response = self.client.get(
            reverse('learn_lab:activity_rate_create',
                    kwargs={'slug': self.activity.slug}))
        self.assertEqual(404, response.status_code)

        response = self.client.get(
            reverse('learn_lab:activity_rate_edit',
                    kwargs={'slug': self.activity.slug}))
        self.assertEqual(404, response.status_code)

        response = self.client.get(
            reverse('learn_lab:activity_rate_delete',
                    kwargs={'slug': self.activity.slug}))
        self.assertEqual(404, response.status_code)
