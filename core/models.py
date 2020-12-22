from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        isnew = not self.id
        super().save(*args, **kwargs)
        if isnew:
            Token.objects.create(user=self)
