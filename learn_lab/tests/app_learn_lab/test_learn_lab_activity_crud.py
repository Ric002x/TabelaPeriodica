import os

from django.conf import settings
from django.urls import resolve, reverse

from learn_lab import views

from .test_learn_lab_base import LearnLabBaseTests


class LearnLabAppActivityCreateTests(LearnLabBaseTests):
    def setUp(self) -> None:
        self.execute_register()
        self.execute_login()
        self.activity_form_data = self.generate_form_activity()
        self.url_activity_create = reverse('learn_lab:activity_create')
        return super().setUp()

    def tearDown(self) -> None:
        media_root = settings.MEDIA_ROOT
        arquive_path = f'{media_root}/learn_lab/files/test.pdf'
        if os.path.exists(arquive_path):
            os.remove(arquive_path)
        return super().tearDown()

    def test_activity_create_view_function(self):
        view = resolve(self.url_activity_create)
        self.assertEqual(view.func, views.activity_create)

    def test_activity_create_template_used(self):
        response = self.client.get(self.url_activity_create)
        self.assertTemplateUsed(
            response, 'learn_lab/pages/learn_lab_activity_create.html')

    def test_activity_create_form_auto_id(self):
        response = self.client.get(self.url_activity_create)
        activity_form = response.context['form']
        self.assertTrue(activity_form.auto_id)

    def test_activity_create_form_instance_is_empty(self):
        response = self.client.get(self.url_activity_create)
        activity_form_instance = response.context['form'].instance.content
        self.assertEqual(activity_form_instance, '')

    def test_activity_create_form_post_sussessful(self):
        response = self.client.post(
            self.url_activity_create, data=self.activity_form_data,
            follow=True)
        msg = 'Atividade criada!'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_activity_create_form_post_invalid(self):
        self.activity_form_data['title'] = ''
        response = self.client.post(
            self.url_activity_create, data=self.activity_form_data,
            follow=True)
        msg = 'Erro no formulário de atividade'
        self.assertIn(msg, response.content.decode('utf-8'))


# Delete Activity Tests
class LearnLabAppActivityDeleteTests(LearnLabBaseTests):
    def setUp(self) -> None:
        self.activity = self.activity_create()
        self.execute_login()
        return super().setUp()

    def tearDown(self) -> None:
        media_root = settings.MEDIA_ROOT
        arquive_path = f'{media_root}/learn_lab/files/test.pdf'
        if os.path.exists(arquive_path):
            os.remove(arquive_path)
        return super().tearDown()

    def test_activy_delete_view_func(self):
        view = resolve(reverse(
            'learn_lab:activity_delete', kwargs={'slug': 'teste'}))
        self.assertEqual(view.func, views.activity_delete)

    def test_activity_delete_not_post_raise_404(self):
        response = self.client.get(reverse(
            'learn_lab:activity_delete', kwargs={'slug': 'teste'}))
        self.assertEqual(404, response.status_code)

    def test_activity_delete_sussessful(self):
        response = self.client.post(reverse(
            'learn_lab:activity_delete', kwargs={'slug': self.activity.slug}),
            follow=True)
        msg = '✅ Atividade deletada com sucesso'
        self.assertIn(msg, response.content.decode('utf-8'))


class LearnLabAppActivityUpdateTests(LearnLabBaseTests):
    def setUp(self) -> None:
        self.activity = self.activity_create(
            is_published=False
        )
        self.execute_login()
        self.url_activity_update = reverse(
            'learn_lab:activity_update', kwargs={'slug': self.activity.slug})
        return super().setUp()

    def tearDown(self) -> None:
        media_root = settings.MEDIA_ROOT
        arquive_path = f'{media_root}/learn_lab/files/test.pdf'
        if os.path.exists(arquive_path):
            os.remove(arquive_path)
        return super().tearDown()

    def test_activity_update_view_function(self):
        view = resolve(self.url_activity_update)
        self.assertEqual(view.func, views.activity_update)

    def test_activity_update_template_used(self):
        response = self.client.get(self.url_activity_update)
        self.assertTemplateUsed(
            response, 'learn_lab/pages/learn_lab_activity_update.html')

    def test_activity_update_raise_404_if_no_activity(self):
        response = self.client.get(reverse(
            'learn_lab:activity_update', kwargs={'slug': 'no-activity'}))
        self.assertEqual(response.status_code, 404)

    def test_activity_update_form_instance(self):
        activity_form_data = self.generate_form_activity()
        response = self.client.get(self.url_activity_update)
        self.assertIn(activity_form_data['title'],
                      response.content.decode('utf-8'))

    def test_activity_update_invalid_form(self):
        activity_form_data = {
            'title': '',
        }
        response = self.client.post(
            self.url_activity_update, data=activity_form_data, follow=True)
        msg = 'Erro na validação da atividade'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_activity_update_form_sussessful(self):
        activity_form_data = self.generate_form_activity()
        activity_form_data['title'] = "NewTitle"
        response = self.client.post(
            self.url_activity_update, data=activity_form_data, follow=True)
        msg = "Atividade atualizada!"
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(activity_form_data['title'],
                      response.content.decode('utf-8'))
