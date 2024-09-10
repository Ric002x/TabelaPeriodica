import os
import random as rd

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from learn_lab.models import Activity, ActivityLevel, ActivitySubject

level_list = [
    '3º ano Ensino Fundamental',
    '4º ano Ensino Fundamental',
    '5º ano Ensino Fundamental',
    '6º ano Ensino Fundamental',
    '7º ano Ensino Fundamental',
    '8º ano Ensino Fundamental',
    '9º ano Ensino Fundamental',
    '1º ano Ensino Médio',
    '2º ano Ensino Médio',
    '3º ano Ensino Médio',
]
subject_list = [
    'Matemática',
    'Ciências',
    'Química',
    'Física',
    'Biologia'
]
file_path = os.path.join(settings.BASE_DIR, 'learn_lab',
                         'tests', 'app_learn_lab', 'files', 'teste.pdf')


class Command(BaseCommand):
    help = "Import activities"

    def handle(self, *args, **kwargs):
        activities_list = []
        for i in range(1, 1001):
            try:
                activity = {
                    'user': User.objects.get(username='Ricardo'),
                    'title': f"Atividade {i}",
                    'description': 'Atividade para testes',
                    'content': "Teste",
                    'subject': rd.choice(subject_list),
                    'level': rd.choice(level_list),
                    'file': file_path,
                }
                activities_list.append(activity)

            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    "User not found"))

        activities_to_create = []
        try:
            for data in activities_list:
                try:
                    subject = ActivitySubject.objects.get(name=data['subject'])
                except ActivitySubject.DoesNotExist:
                    self.stdout.write(self.style.ERROR(
                        f"Subject {data['subject']} not found"))
                    continue

                try:
                    level = ActivityLevel.objects.get(name=data['level'])
                except ActivityLevel.DoesNotExist:
                    self.stdout.write(self.style.ERROR(
                        f"Level {data['level']} not found"))
                    continue

                activity_to_create = Activity(
                    user=data['user'],
                    title=data['title'],
                    slug=slugify(data['title']),
                    description=data['description'],
                    file=data['file'],
                    subject=subject,
                    content=data['content'],
                    level=level,
                    is_published=True,
                )
                activities_to_create.append(activity_to_create)

        except ActivitySubject.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                f"User {data['subject']} not found"))

        if activities_to_create:
            Activity.objects.bulk_create(activities_to_create)
            self.stdout.write(self.style.SUCCESS(
                f'Successfully created {len(
                    activities_to_create)} activities'))
