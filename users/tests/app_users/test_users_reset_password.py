import re

from django.contrib.auth.models import User
from django.core import mail
from django.urls import resolve, reverse

from users import views

from .test_app_users_base import TestBaseUsersApp


class ForgotMyPasswordTests(TestBaseUsersApp):
    def setUp(self) -> None:
        self.url = reverse("users:forgot_my_password")
        return super().setUp()

    def test_forget_my_password_function_view(self):
        view = resolve(self.url)
        self.assertEqual(views.forgot_my_password, view.func)

    def test_forget_my_password_return_200_and_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "users/pages/forgot_my_password.html")

    def test_forget_my_password_can_not_access_if_user_is_logged(self):
        self.execute_register()
        self.execute_login()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,  # type: ignore
            '/usuarios/perfil/username/publicacoes/')

    def test_forget_my_password_not_email_error(self):
        response = self.client.post(self.url, data={
            'email': ""
        }, follow=True)
        msg = "Por favor, insira um e-mail válido."
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_forget_my_password_user_not_found(self):
        response = self.client.post(self.url, data={
            'email': "teste@email.com"
        }, follow=True)
        msg = "Falha na solicitação! Certifique-se que solicitou" \
            " para o email correto"
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_forget_my_password_create_reset_link(self):
        self.execute_register()

        self.client.post(self.url, data={
            'email': "teste@email.com"
        })

        email = mail.outbox[0]
        self.assertIn(
            "http://testserver/usuarios/redefinir-senha/?token=", email.body)

    def test_forget_my_password_send_email_successful(self):
        self.execute_register()
        self.client.post(self.url, data={
            'email': "teste@email.com"
        })

        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox[0]
        self.assertEqual(email.to, ["teste@email.com"])
        self.assertIn("Solicitação de Alteração de Senha", email.subject)
        self.assertIn("Houve uma solicitação de ", email.body)


class ResetPasswordTests(TestBaseUsersApp):
    def setUp(self) -> None:
        self.execute_register()
        self.user = User.objects.filter(email="teste@email.com").first()

        self.client.post(reverse("users:forgot_my_password"), data={
            'email': "teste@email.com"
        })

        email = mail.outbox[0]
        extracted_text = re.search(r'https?://\S+', email.body)

        # Captura o link encontrado ou retorna uma mensagem
        self.link = extracted_text.group(
            0) if extracted_text else "Nenhum link encontrado."

        self.password_form = {
            "new_password": "ValidPassword1",
            "repeat_password": "ValidPassword1"
        }

        return super().setUp()

    def test_reset_password_can_not_access_if_user_is_logged(self):
        self.execute_login()
        response = self.client.get(self.link, follow=True)
        msg = "usuário já logado"
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_reset_password_redirects_if_not_token(self):
        response = self.client.get(
            reverse("users:reset_password"), follow=True)
        msg = "Falha na solicitação. Por favor, tente novamente"
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_reset_password_returns_200_if_valid_url(self):
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)

    def test_reset_password_post_error_differente_passwords(self):
        self.password_form['repeat_password'] = "different_password"
        response = self.client.post(
            self.link, self.password_form)

        self.assertIn("As senhas precisam ser iguais",
                      response.content.decode('utf-8'))

    def test_reset_password_post_error_invalid_regex_password(self):
        self.password_form['new_password'] = "invalidpassword"
        response = self.client.post(
            self.link, self.password_form)

        self.assertIn("A senha deve contar pelo menos 8 caracteres, "
                      "incluindo letras maiúsculas e números",
                      response.content.decode('utf-8'))

    def test_reset_password_successfull(self):
        response = self.client.post(
            self.link, self.password_form, follow=True)

        msg = "Senha redefinida com sucesso." \
            " Faça login para continuar"
        self.assertIn(msg, response.content.decode('utf-8'))
