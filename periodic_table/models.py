import json
import os

from django.db import models

elements_category_str = os.environ.get('ELEMENTS_CATEGORIES')

# Verifica se a variável de ambiente não é None antes de carregar
if elements_category_str:
    elements_category = json.loads(elements_category_str)
else:
    ...


class Element(models.Model):
    name = models.CharField(unique=True, max_length=50)
    slug = models.SlugField(unique=True)
    symbol = models.CharField(default='', max_length=2)
    description = models.TextField(default='')
    cover_image = models.ImageField(
        upload_to='periodic_table/elements_cover/',
        blank=True,
        null=True,
        default='')
    bohr_model = models.ImageField(
        upload_to='periodic_table/elements_bohr_model/',
        blank=True,
        null=True,
        default=''
    )
    atomic_number = models.IntegerField(default=0)
    atomic_mass = models.FloatField(default=0)
    electrons_number = models.IntegerField(default=0)
    neutrons_number = models.IntegerField(default=0)
    density = models.FloatField(default=0, blank=True)  # g/cm³
    melting_point = models.FloatField(default=0, blank=True)  # °C
    boiling_point = models.FloatField(default=0, blank=True)  # °C
    state_matter = models.CharField(
        max_length=20, default='')  # Solid, Gas, Liquid
    electronic_configuration = models.TextField(default='')   # 1s²...
    electron_distribution = models.CharField(default='', max_length=50)
    ionic_states = models.CharField(
        max_length=100, blank=True)  # 1+, 2+...
    history_and_discovery = models.TextField(default='', blank=True)
    chemical_properties = models.TextField(default='', blank=True)
    usage = models.TextField(default='', blank=True)
    extra_information = models.TextField(default='', blank=True)

    def __str__(self) -> str:
        return self.name

    def melting_point_fahrenheit(self):
        return round(self.melting_point * 9/5 + 32, 3)

    def melting_point_kelvin(self):
        return round(self.melting_point + 273.15, 3)

    def boiling_point_fahrenheit(self):
        return round(self.boiling_point * 9/5 + 32, 3)

    def boiling_point_kelvin(self):
        return round(self.boiling_point + 273.15, 3)

    def get_css_class(self):
        for category, symbols in elements_category.items():
            if self.symbol in symbols:
                return category
        return 'unknown'
