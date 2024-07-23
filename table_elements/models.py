from django.db import models
import os
import json

# Create your models here.
elements_category = json.loads(os.environ.get('ELEMENTS_CATEGORIES'))


class Elements(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True)
    symbol = models.CharField(max_length=5)
    element_cover = models.ImageField(
        upload_to='table_elements/elements_cover/',
        blank=True,
        default='')
    bohr_model = models.ImageField(
        upload_to='table_elements/elements_bohr_model/',
        blank=True,
        default=''
    )
    atomic_number = models.IntegerField(default=0)
    atomic_mass = models.FloatField(default=0)
    electrons_number = models.IntegerField(default=0)
    neutrons_number = models.IntegerField(default=0)
    density = models.FloatField(default=0)  # g/cm³
    melting_point = models.FloatField(default=0)  # °C
    boiling_point = models.FloatField(default=0)  # °C
    state_matter = models.CharField(
        max_length=20, default='')  # Solid, Gas, Liquid
    electronic_configuration = models.TextField(default='')   # 1s²...
    ionic_states = models.CharField(
        max_length=100, blank=True)  # 1+, 2+...
    discoverer = models.CharField(max_length=100, blank=True)
    year_discovered = models.IntegerField(blank=True, null=True)

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
