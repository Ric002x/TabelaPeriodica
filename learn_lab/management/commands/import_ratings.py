from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from learn_lab.models import Activity, ActivityRating

ratings_for_id_1 = {
    'rating1': {
        'user': "David",
        'rating': 5,
        'comment': ('Excelente atividade! Explica muito bem cada fase do '
                    'ciclo da água e a relação com o meio ambiente. As '
                    'imagens e exemplos são claros e facilitam o '
                    'entendimento.')
    },
    'rating2': {
        'user': "Alice",
        'rating': 4,
        'comment': ('Atividade boa, mas poderia incluir mais exemplos '
                    'práticos sobre a influência do ciclo da água no '
                    'clima das diferentes regiões.')
    }
}

ratings_for_id_2 = {
    'rating1': {
        'user': "Bob",
        'rating': 5,
        'comment': ('Muito didática! A explicação sobre os átomos e suas'
                    ' partículas foi bem clara. O uso da Tabela Periódica '
                    'como apoio ajudou muito.')
    },
    'rating2': {
        'user': "Charlie",
        'rating': 3,
        'comment': ('A atividade é boa, mas alguns alunos acharam a '
                    'explicação sobre números atômicos um pouco confusa.')
    },
    'rating3': {
        'user': "Alice",
        'rating': 4,
        'comment': ('Ótima introdução, mas seria interessante incluir '
                    'mais exercícios para reforçar a aprendizagem.')
    },
}

ratings_for_id_3 = {
    'rating1': {
        'user': "Barbara",
        'rating': 4,
        'comment': ('Gostei muito da abordagem simplificada dos sistemas '
                    'do corpo humano. Facilita o entendimento para quem '
                    'está começando a aprender o conteúdo.')
    },
    'rating2': {
        'user': "Alice",
        'rating': 5,
        'comment': ('Muito completa! Abordou todos os sistemas de forma '
                    'clara, e as doenças relacionadas foram um '
                    'ótimo complemento.')
    },
    'rating3': {
        'user': "Charlie",
        'rating': 4,
        'comment': ('Achei que a parte sobre o sistema nervoso poderia '
                    'ter mais detalhes, mas no geral, é uma boa atividade.')
    },
    'rating4': {
        'user': "David",
        'rating': 5,
        'comment': ('Ótima atividade, ajudou muito na revisão dos '
                    'principais sistemas do corpo humano!')
    }
}

ratings_for_id_4 = {
    'rating1': {
        'user': "Bob",
        'rating': 4,
        'comment': ('Muito útil para aplicar em problemas práticos! Achei '
                    'que alguns exemplos poderiam ser mais detalhados.')
    },
    'rating2': {
        'user': "David",
        'rating': 3,
        'comment': ('Atividade interessante, mas faltaram mais exercícios '
                    'para consolidar o conceito de forma prática.')
    }
}

ratings_for_id_5 = {
    'rating1': {
        'user': "Charlie",
        'rating': 5,
        'comment': ('Excelente! A abordagem com exemplos e experimentos '
                    'foi essencial para fixar o conteúdo. As leis de '
                    'Newton ficaram muito mais claras com essa atividade.')
    },
    'rating2': {
        'user': "David",
        'rating': 4,
        'comment': ('A atividade foi boa, mas alguns alunos acharam '
                    'os conceitos de ação e reação um pouco '
                    'abstratos. Poderia ter mais exemplos.')
    },
    'rating3': {
        'user': "Barbara",
        'rating': 5,
        'comment': ('Super didática! Os alunos conseguiram entender '
                    'e aplicar as Leis de Newton em situações do cotidiano.')
    }
}


class Command(BaseCommand):
    help = 'import ratings'

    def handle(self, *args, **kwargs):
        for i in range(1, 6):
            try:
                Activity.objects.get(id=i)
            except ObjectDoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f"Activity with id {i} not found"))
                break

        activity1 = Activity.objects.get(id=1)
        ratings_to_create = []
        for key, value in ratings_for_id_1.items():
            rating = ActivityRating(
                activity=activity1,
                user=User.objects.get(username=value['user']),
                rating=value['rating'],
                comment=value['comment'],
            )
            ratings_to_create.append(rating)

        activity2 = Activity.objects.get(id=2)
        for key, value in ratings_for_id_2.items():
            rating = ActivityRating(
                activity=activity2,
                user=User.objects.get(username=value['user']),
                rating=value['rating'],
                comment=value['comment'],
            )
            ratings_to_create.append(rating)

        activity3 = Activity.objects.get(id=3)
        for key, value in ratings_for_id_3.items():
            rating = ActivityRating(
                activity=activity3,
                user=User.objects.get(username=value['user']),
                rating=value['rating'],
                comment=value['comment'],
            )
            ratings_to_create.append(rating)

        activity4 = Activity.objects.get(id=4)
        for key, value in ratings_for_id_4.items():
            rating = ActivityRating(
                activity=activity4,
                user=User.objects.get(username=value['user']),
                rating=value['rating'],
                comment=value['comment'],
            )
            ratings_to_create.append(rating)

        activity5 = Activity.objects.get(id=5)
        for key, value in ratings_for_id_5.items():
            rating = ActivityRating(
                activity=activity5,
                user=User.objects.get(username=value['user']),
                rating=value['rating'],
                comment=value['comment'],
            )
            ratings_to_create.append(rating)

        if ratings_to_create:
            ActivityRating.objects.bulk_create(ratings_to_create)
            self.stdout.write(self.style.SUCCESS(
                f'Successfully created {len(
                    ratings_to_create)} ratings'))
        else:
            self.stdout.write(self.style.WARNING('No ratings to create'))
