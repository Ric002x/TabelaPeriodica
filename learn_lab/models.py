import os
import random
import string

import fitz
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
random_string = ''.join(random.choices(string.ascii_letters, k=5))


def file_upload(instance, filename):
    filename, ext = os.path.splitext(filename)
    filename = {slugify(filename)}
    return f'learn_lab/files/{filename}{ext}'


class ActivitySubject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class ActivityLevel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return (self.name)


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField()
    file = models.FileField(
        upload_to=file_upload,
        blank=True,
        default='',
    )
    thumbnail = models.ImageField(
        upload_to='learn_lab/thumbnails/',
        blank=True,
        default=''
    )
    subject = models.ForeignKey(
        ActivitySubject, on_delete=models.SET_NULL,
        blank=True, null=True, default=None)
    content = models.CharField(max_length=100)
    level = models.ForeignKey(
        ActivityLevel, on_delete=models.SET_NULL,
        blank=True, null=True, default=None)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("learn_lab:learn_lab_activity",
                       kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(f'{self.title}-{random_string}')
            str(slug)
            self.slug = slug

        super().save(*args, **kwargs)

        if self.file:
            pdf = fitz.open(self.file.path)
            page = pdf.load_page(0)
            pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))  # type: ignore
            file_slug = slugify(self.file.name).replace("learn_labfiles", "") \
                .replace("pdf", "")
            save_path = os.path.join(
                settings.MEDIA_ROOT, 'learn_lab', 'thumbnails')
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            pix.save(f'{save_path}/{file_slug}.png')

            self.thumbnail = f'learn_lab/thumbnails/{file_slug}.png'

        super().save(update_fields=['thumbnail'])


class ActivityRating(models.Model):
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name='rating')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    rating = models.PositiveIntegerField(
        choices=((1, '1 star'), (2, '2 star'), (3, '3 star'),
                 (4, '4 star'), (5, '5 star')))
    comment = models.TextField(blank=True, null=True, max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'activity'],
                name='unique_user_activity_rating')
        ]
