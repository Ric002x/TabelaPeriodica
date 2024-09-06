from django.core.management.base import BaseCommand
from learn_lab.models import ActivitySubject
from django.db import transaction


class Command(BaseCommand):
    help = "Import activity levels"

    def handle(self, *args, **kwargs):
        subject_list = [
            'Matemática',
            'Ciências',
            'Química',
            'Física',
            'Biologia'
        ]
        try:
            with transaction.atomic():
                subjects_to_create = []
                existing_subjects = ActivitySubject.objects.values_list(
                    'name', flat=True)

                for subject_name in subject_list:
                    if subject_name not in existing_subjects:
                        subject_name = ActivitySubject(name=subject_name)
                        subjects_to_create.append(subject_name)

                if subjects_to_create:
                    ActivitySubject.objects.bulk_create(subjects_to_create)
                    self.stdout.write(self.style.SUCCESS('Successfully imported activity levels'))   # noqa: E501
                else:
                    self.stdout.write(self.style.WARNING('No new activity levels to import'))   # noqa: E501

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))
