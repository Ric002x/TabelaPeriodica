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

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            str(slug)
            self.slug = slug

        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("learn_lab:learn_lab_activity",
                       kwargs={"slug": self.slug})
