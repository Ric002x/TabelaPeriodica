from django.core.management.base import BaseCommand
from django.db import transaction

from learn_lab.models import ActivityLevel


class Command(BaseCommand):
    help = "Import activity levels"

    def handle(self, *args, **kwargs):
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
        try:
            with transaction.atomic():
                levels_to_create = []
                existing_levels = ActivityLevel.objects.values_list(
                    'name', flat=True)

                for level_name in level_list:
                    if level_name not in existing_levels:
                        level_name = ActivityLevel(
                            name=level_name)
                        levels_to_create.append(level_name)

                if levels_to_create:
                    ActivityLevel.objects.bulk_create(levels_to_create)
                    self.stdout.write(self.style.SUCCESS('Successfully imported activity levels'))   # noqa: E501
                else:
                    self.stdout.write(self.style.WARNING('No new activity levels to import'))   # noqa: E501

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))
