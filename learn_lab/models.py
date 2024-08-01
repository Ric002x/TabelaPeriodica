from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    file = models.FileField(
        upload_to='learn_lab/files/',
        blank=True,
        null=True,
        default=None,
        )
    subject = models.ForeignKey(
        ActivitySubject, on_delete=models.SET_NULL,
        blank=True, null=True, default=None)
    content = models.CharField(max_length=50)
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
            slug = slugify(self.title)
            str(slug)
            self.slug = slug
        super().save(*args, **kwargs)
