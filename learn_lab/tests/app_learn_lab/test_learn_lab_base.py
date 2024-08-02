from django.test import TestCase
from learn_lab.models import Activity, ActivityLevel, ActivitySubject
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io


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
        description='activity Description',
        subject_data=None,
        content='Activity content',
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
            content=content,
            level=self.create_level(**level_data),
            title=title,
            description=description,
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
        }
        return register_form_data

    def generate_form_login(self):
        login_form_data = {
            'username': 'username',
            'password': 'Password123',
        }
        return login_form_data

    def generate_form_activity(self):
        subject = self.create_subject()
        level = self.create_level()
        pdf_file = self.create_pdf_file()
        activity_form_data = {
            'title': 'Activity Title',
            'description': 'activity Description',
            'subject': subject.id,
            'content': 'Activity content',
            'level': level.id,
            'file': pdf_file,
        }
        return activity_form_data

    def create_pdf_file(self):
        # Cria um buffer de memória
        buffer = io.BytesIO()

        # Cria um PDF no buffer
        p = canvas.Canvas(buffer, pagesize=letter)
        p.drawString(100, 750, "Hello World")
        p.showPage()
        p.save()

        # Retorna um SimpleUploadedFile para o teste
        buffer.seek(0)  # Move o cursor para o início do buffer
        return SimpleUploadedFile(
            'test_file.pdf',
            buffer.read(),
            content_type='application/pdf'
        )

    def execute_register(self):
        self.client.post(reverse(
            'users:register_create'), data=self.generate_form_register())

    def execute_login(self):
        self.client.post(reverse(
            'users:login_create'), data=self.generate_form_login())


class LearnLabBaseTests(TestCase, ActivityMixin):
    def setUp(self) -> None:
        return super().setUp()
