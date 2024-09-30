import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from learn_lab.models import Activity, ActivityLevel, ActivitySubject


class ActivityMixin:
    def create_subject(self, name='Ciências'):
        subject = ActivitySubject.objects.create(
            name=name,
        )
        subject.full_clean()
        subject.save()
        return subject

    def create_level(self, name='9º ano EF'):
        level = ActivityLevel.objects.create(
            name=name,
        )
        level.full_clean()
        level.save()
        return level

    def create_user(
        self,
        first_name='user',
        last_name='name',
        username='username',
        password='Password123',
        email='teste@email.com'
    ):
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )
        user.set_password(password)
        user.full_clean()
        user.save()
        return user

    def activity_create(
        self,
        user_data=None,
        title='Activity Title',
        description='activity Description',
        subject_data=None,
        content='Activity content',
        level_data=None,
        is_published=True,
        file=None,
        simple=False,
    ):
        if user_data is None:
            user_data = {}
        if subject_data is None:
            subject_data = {}
        if level_data is None:
            level_data = {}

        if simple is False:

            activity = Activity.objects.create(
                user=self.create_user(**user_data),
                subject=self.create_subject(**subject_data),
                content=content,
                level=self.create_level(**level_data),
                title=title,
                description=description,
                is_published=is_published,
                file=file,
            )
        elif simple is True:
            activity = Activity.objects.create(
                user=User.objects.get(id=1),
                title=title,
                description=description,
                content=content,
                is_published=is_published,
            )
        activity.full_clean()
        activity.save()
        return activity

    def generate_form_register(self):
        register_form_data = {
            'first_name': 'User',
            'last_name': 'Name',
            'username': 'username',
            'password': 'Password123',
            'password2': 'Password123',
            'email': 'teste@email.com',
            'agree_to_terms': True,
        }
        return register_form_data

    def generate_form_login(self):
        login_form_data = {
            'username': 'username',
            'password': 'Password123',
        }
        return login_form_data

    def generate_form_activity(self):
        pdf_path = os.path.join(
            settings.BASE_DIR, 'learn_lab', 'tests', 'app_learn_lab',
            'files', 'teste.pdf')
        with open(pdf_path, 'rb') as f:
            pdf_file = SimpleUploadedFile(
                'test.pdf',
                f.read(),
                content_type='application/pdf'
            )
        activity_form_data = {
            'title': 'Activity Title',
            'description': 'activity Description',
            'content': 'Activity content',
            'file': pdf_file,
        }
        if len(ActivitySubject.objects.all()) == 0:
            subject = self.create_subject()
            activity_form_data['subject'] = subject.id  # type: ignore
        else:
            pass
        if len(ActivityLevel.objects.all()) == 0:
            level = self.create_level()
            activity_form_data['level'] = level.id  # type: ignore
        else:
            pass

        return activity_form_data

    def execute_register(self):
        self.client.post(reverse(  # type: ignore
            'users:register_create'), data=self.generate_form_register())

    def execute_login(self):
        self.client.post(reverse(  # type: ignore
            'users:login_create'), data=self.generate_form_login())

    def generate_form_rating(self):
        rating_form_data = {
            'rating': 3,
            'comment': 'comment',
        }
        return rating_form_data

    def upload_file(self):
        pdf_path = os.path.join(
            settings.BASE_DIR, 'learn_lab', 'tests', 'app_learn_lab',
            'files', 'teste.pdf')
        with open(pdf_path, 'rb') as f:
            pdf_file = SimpleUploadedFile(
                'test.pdf',
                f.read(),
                content_type='application/pdf'
            )
        activity = Activity.objects.create(
            file=pdf_file,
        )
        return activity

    def bulk_create_activity(
            self, range, create_user=True, subject=None, level=None):
        if create_user is True:
            user = User.objects.create(
                username="Test"
            )
        else:
            user = User.objects.get(id=1)
        for i in range:
            Activity.objects.create(
                title=f"Activity {i}",
                user=user,
                subject=subject,
                level=level,
                is_published=True
            )


class LearnLabBaseTests(TestCase, ActivityMixin):
    def setUp(self) -> None:
        return super().setUp()
