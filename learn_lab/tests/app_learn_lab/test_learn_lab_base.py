from django.test import TestCase
from learn_lab.models import Activity, ActivityLevel, ActivitySubject
from django.contrib.auth.models import User


class ActivityMixin:
    def create_subject(self, name='Ciências'):
        subject = ActivitySubject.objects.create(
            name=name
        )
        subject.full_clean()
        subject.save()
        return subject

    def create_level(self, name='9º ano EF'):
        level = ActivityLevel.objects.create(
            name=name
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
        description='activity description',
        subject_data=None,
        level_data=None,
        is_published=True,
    ):
        if user_data is None:
            user_data = {}
        if subject_data is None:
            subject_data = {}
        if level_data is None:
            level_data = {}

        activity = Activity.objects.create(
            user=self.create_user(**user_data),
            subject=self.create_subject(**subject_data),
            level=self.create_level(**level_data),
            title=title,
            description=description,
            is_published=is_published,
        )
        activity.full_clean()
        activity.save()
        return activity


class LearnLabBaseTests(TestCase, ActivityMixin):
    def setUp(self) -> None:
        return super().setUp()
