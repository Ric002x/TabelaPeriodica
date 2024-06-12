from django.db import models
from django.urls import reverse

# Create your models here.


class Elements(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30)
    simbol = models.CharField(max_length=5)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("tabela_elementos:single_element",
                       kwargs={"slug": self.slug})
