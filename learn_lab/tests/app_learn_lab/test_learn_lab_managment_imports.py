from django.core.management import call_command
from django.test import TestCase
from learn_lab.models import ActivityLevel, ActivitySubject


class ImportActivityLevelsCommandTests(TestCase):
    def setUp(self) -> None:
        # Limpar os níveis de atividades existentes
        # para garantir um ambiente de teste limpo
        ActivityLevel.objects.all().delete()
        return super().setUp()

    def test_import_activity_levels(self):
        # Contar o número de níveis de atividades antes da execução do comando
        initial_count = ActivityLevel.objects.count()

        # Executar o comando de gerenciamento
        call_command('import_levels')

        # Contar o número de níveis de atividades após a execução do comando
        final_count = ActivityLevel.objects.count()

        # Níveis esperados
        expected_levels = [
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

        # Verificar se os níveis esperados foram adicionados ao banco de dados
        for level_name in expected_levels:
            self.assertTrue(
                ActivityLevel.objects.filter(name=level_name).exists())

        # Verificar se o número de níveis de atividades
        # aumentou pelo número esperado
        self.assertEqual(final_count, initial_count + len(expected_levels))


class ImportActivitySubjectsCommandTests(TestCase):
    def setUp(self):
        # Limpar os assuntos existentes para
        # garantir um ambiente de teste limpo
        ActivitySubject.objects.all().delete()
        return super().setUp()

    def test_import_activity_subjects(self):
        # Contar o número de assuntos antes da execução do comando
        initial_count = ActivitySubject.objects.count()

        # Executar o comando de gerenciamento
        call_command('import_subjects')

        # Contar o número de assuntos após a execução do comando
        final_count = ActivitySubject.objects.count()

        # Assuntos esperados
        expected_subjects = [
            'Matemática',
            'Ciências',
            'Química',
            'Física',
            'Biologia'
        ]

        # Verificar se os assuntos esperados foram
        # adicionados ao banco de dados
        for subject_name in expected_subjects:
            self.assertTrue(
                ActivitySubject.objects.filter(name=subject_name).exists())

        # Verificar se o número de assuntos aumentou pelo número esperado
        self.assertEqual(final_count, initial_count + len(expected_subjects))
