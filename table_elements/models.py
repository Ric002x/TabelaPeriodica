from django.db import models
from django.urls import reverse

# Create your models here.
ametal = ['H', 'C', 'N', 'O', 'P', 'S', 'Se']
alcaline_metal = ['Li', 'Na', 'K', 'Rb', 'Cs', 'Fr']
alcaline_metal2 = ['Be', 'Mg', 'Ca', 'Sr', 'Ba', 'Ra']
semiconductors = ['Al', 'Ga', 'In', 'Sn', 'Tl', 'Nh',
                  'Fl', 'Pb', 'Bi', 'Mc', 'Lv']
trans_metals = [
    'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
    'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd',
    'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg',
    'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn'
]
semimetals = ['B', 'Si', 'Ge', 'As', 'Sb', 'Te', 'Po']
halogens = ['Cl', 'F', 'Br', 'I', 'At', 'Ts']
nobel_gas = ['He', 'Ne', 'Ar', 'Kr', 'Xe', 'Rn', 'Og']
lantanides = [
    'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy',
    'Ho', 'Er', 'Tm', 'Yb', 'Lu'
]
actinides = [
    'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf',
    'Es', 'Fm', 'Md', 'No', 'Lr'
]


class Elements(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True)
    simbol = models.CharField(max_length=5)
    element_cover = models.ImageField(
        upload_to='table_elements/elements_cover/',
        blank=True,
        default='')
    atomic_number = models.IntegerField()
    atomic_mass = models.FloatField()

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("table_elements:single_element",
                       kwargs={"slug": self.slug})

    def get_css_class(self):
        if self.simbol in ametal:
            return 'ametal'

        if self.simbol in alcaline_metal:
            return 'metal-alcaline'

        if self.simbol in alcaline_metal2:
            return 'metal-alcaline-2'

        if self.simbol in nobel_gas:
            return 'nobel-gas'

        if self.simbol in trans_metals:
            return 'trans-metal'

        if self.simbol in semimetals:
            return 'semimetal'

        if self.simbol in halogens:
            return 'halogen'

        if self.simbol in semiconductors:
            return 'semiconductor'

        if self.simbol in actinides:
            return 'actinide'

        if self.simbol in lantanides:
            return 'lantanide'
