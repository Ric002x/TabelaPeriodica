from .test_app_users_base import TestBaseUsersApp
from users.forms import RegisterForm


class UsersAppModelProfileTests(TestBaseUsersApp):
    def setUp(self) -> None:
        form = RegisterForm(self.generate_form_register())
        self.user = form.save(commit=False)
        self.user.save()
        return super().setUp()

    def test_user_return_username_str(self):
        user = self.user
        self.assertEqual(str(user.profile.user), 'username')

    def test_model_profile_default_img(self):
        user = self.user
        self.assertEqual(user.profile.avatar.url, '/media/users/default.png')
