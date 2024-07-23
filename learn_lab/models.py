from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from pdf2image import convert_from_path
from PIL import Image
from django.conf import settings
import os

# Create your models here.


class ActivitySubject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class ActivityLevel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return (self.name)


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    file = models.FileField(
        upload_to='learn_lab/files/',
        blank=True,
        default='',
        )
    subject = models.ForeignKey(
        ActivitySubject, on_delete=models.CASCADE, related_name='activities')
    level = models.ForeignKey(
        ActivityLevel, on_delete=models.CASCADE, related_name='activities')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(
        upload_to='learn_lab/files/thumbnails/', default='', blank=True)

    def __str__(self):
        return str(self.title)    

    def get_absolute_url(self):
        return reverse("learn_lab:learn_lab_activity",
                       kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            str(slug)
            self.slug = slug

        if not self.thumbnail:
            file_path = self.file.path

            thumbnail_filename = f'{os.path.splitext(self.file.name)[0]}.jpeg'
            thumbnail_path = os.path.join(
                settings.MEDIA_ROOT, 'learn_lab/files/thumbnails/',
                thumbnail_filename)
            os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)

            try:
                poppler_path = os.environ.get("POPPER_PATH")
                pages = convert_from_path(
                    file_path, first_page=1, last_page=1,
                    poppler_path=poppler_path)
                if pages:
                    image = pages[0]
                    image.thumbnail(size=(1050, 1485))
                    image.save(thumbnail_path, "JPEG")
                    self.thumbnail = os.path.join(
                        'learn_lab/files/thumbnails/', thumbnail_filename)
            except Exception as e:
                print(f"Erro ao gerar a miniatura: {e}")
        super().save(*args, **kwargs)
