import pandas as pd
from django.core.management.base import BaseCommand

from periodic_table.models import Element


class Command(BaseCommand):
    help = 'Import elements from CSV'

    def handle(self, *args, **kwargs):
        try:
            # Caminho para o arquivo CSV
            file_path = 'periodic_table/management/commands/elements.csv'

            # Lendo o arquivo CSV
            file = pd.read_csv(file_path)

            # Verificando as colunas no CSV
            expected_columns = {'name', 'slug', 'simbol', 'atomic_number', 'atomic_mass',   # noqa: E501
                                'electrons_number', 'neutrons_number', 'density',   # noqa: E501
                                'melting_point', 'boiling_point', 'state_matter',   # noqa: E501
                                'electronic_configuration', 'electron_distribution',    # noqa: E501
                                'ionic_states'}

            if not expected_columns.issubset(file.columns):
                raise ValueError("CSV file is missing one or more required columns.")   # noqa: E501

            elements = []
            for row in file.index:
                # Criando um novo elemento
                element = Element(
                    name=file.loc[row, 'name'],
                    slug=file.loc[row, 'slug'],
                    symbol=file.loc[row, 'simbol'],
                    atomic_number=file.loc[row, 'atomic_number'],
                    atomic_mass=file.loc[row, 'atomic_mass'],
                    electrons_number=file.loc[row, 'electrons_number'],
                    neutrons_number=file.loc[row, 'neutrons_number'],
                    density=file.loc[row, 'density'],
                    melting_point=file.loc[row, 'melting_point'],
                    boiling_point=file.loc[row, 'boiling_point'],
                    state_matter=file.loc[row, 'state_matter'],
                    electronic_configuration=file.loc[row, 'electronic_configuration'],   # noqa: E501
                    electron_distribution=file.loc[row, 'electron_distribution'],   # noqa: E501
                    ionic_states=file.loc[row, 'ionic_states'],
                )
                elements.append(element)

            # Salvando todos os elementos de uma vez
            Element.objects.bulk_create(elements)

            self.stdout.write(self.style.SUCCESS('Successfully imported elements from CSV'))   # noqa: E501

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))
