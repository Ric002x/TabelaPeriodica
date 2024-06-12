from django.db import models
from django.urls import reverse

# Create your models here.


class Elements(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True)
    simbol = models.CharField(max_length=5)
    element_cover = models.ImageField(
        upload_to='tabaela_elementos/elements_cover/',
        blank=True,
        default='')
    atomic_number = models.IntegerField()
    atomic_mass = models.FloatField()

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("tabela_elementos:single_element",
                       kwargs={"slug": self.slug})
