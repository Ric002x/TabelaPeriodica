
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
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


class Command(BaseCommand):
    help = "Import activities"

    def handle(self, *args, **kwargs):
        activity1 = {
            'user': "Ricardo",
            'title': 'O ciclo da água',
            'description': "Esta atividade aborda o ciclo da água, destacando \
                os processos de evaporação, condensação e precipitação. Os \
                alunos aprenderão como a água se move através da atmosfera, \
                solo e corpos d'água, e sua importância para o equilíbrio \
                ecológico. A atividade também foca na relação entre o ciclo \
                da água e as mudanças climáticas, com ênfase na importância \
                da preservação dos recursos hídricos.",
            'content': "Sustentabilidade",
            'subject': 'Ciências',
            'level': '8º ano Ensino Fundamental',
        }

        activity2 = {
            'user': "Ricardo",
            'title': 'Introdução aos átomos',
            'description': "Esta atividade explora os conceitos básicos da \
                estrutura atômica. Os alunos vão aprender sobre as partículas \
                subatômicas (prótons, nêutrons e elétrons), entender os \
                números atômicos e de massa, e como esses conceitos formam \
                a base da Química moderna. Também há uma introdução à Tabela \
                Periódica, que ajuda a classificar os elementos.",
            'content': "Átomos",
            'subject': 'Química',
            'level': '9º ano Ensino Fundamental',
        }

        activity3 = {
            'user': "Ricardo",
            'title': 'Sistemas do corpo humano',
            'description': "Esta atividade visa ensinar sobre os diferentes \
                sistemas do corpo humano, como o sistema digestório, \
                circulatório, respiratório, e nervoso. Os alunos \
                aprenderão as funções de cada sistema e sua importância \
                para a saúde humana. Também discutiremos doenças comuns \
                relacionadas a esses sistemas e como preveni-las.",
            'content': "Fisiologia",
            'subject': 'Biologia',
            'level': '1º ano Ensino Médio',
        }

        activity4 = {
            'user': "Ricardo",
            'title': 'O teorema de Pitágoras',
            'description': "Esta atividade oferece uma introdução ao Teorema \
                de Pitágoras, demonstrando sua aplicação em triângulos \
                retângulos. Os alunos aprenderão a usar o teorema para \
                calcular o comprimento dos lados em figuras geométricas, \
                com exemplos práticos e problemas que envolvem situações \
                do cotidiano.",
            'content': "Mecânica",
            'subject': 'Física',
            'level': '7º ano Ensino Fundamental',
        }

        activity5 = {
            'user': "Ricardo",
            'title': 'Leis de Newton',
            'description': "Nesta atividade, os alunos aprenderão sobre as \
                três Leis de Newton, que formam a base da mecânica clássica. \
                Serão discutidos conceitos como inércia, aceleração, e \
                ação-reação, com exemplos práticos de como essas leis se \
                aplicam no dia a dia. A atividade inclui experimentos simples \
                para reforçar o entendimento.",
            'content': "Geometria",
            'subject': 'Matemática',
            'level': '2º ano Ensino Médio',
        }

        activities_list = [activity1, activity2,
                           activity3, activity4, activity5]
        activities_to_create = []
        for activity in activities_list:
            try:
                user = User.objects.get(username=activity['user'])
            except ObjectDoesNotExist:
                self.stdout.write(self.style.ERROR(
                    "User not found"))

            try:
                subject = ActivitySubject.objects.get(name=activity['subject'])
            except ObjectDoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f"Subject {activity['subject']} not found"))

            try:
                level = ActivityLevel.objects.get(name=activity['level'])
            except ObjectDoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f"Level {activity['level']} not found"))

            activity = Activity(
                user=user,
                title=activity['title'],
                slug=slugify(activity['title']),
                description=activity['description'],
                subject=subject,
                content=activity['content'],
                level=level,
                is_published=True,
            )
            activities_to_create.append(activity)

        if activities_to_create:
            Activity.objects.bulk_create(activities_to_create)
            self.stdout.write(self.style.SUCCESS(
                f'Successfully created {len(
                    activities_to_create)} activities'))
