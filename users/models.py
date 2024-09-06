from django.contrib.auth.models import User
from django.db import models
from PIL import Image

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='users/avatars/',
        blank=True,
        null=True,
        default='')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()

        try:
            img = Image.open(self.avatar.path)

            if img.size != (100, 100):
                new_img = (100, 100)
                img.thumbnail(new_img)
                img.save(self.avatar.path)
        except ValueError:
            ...
