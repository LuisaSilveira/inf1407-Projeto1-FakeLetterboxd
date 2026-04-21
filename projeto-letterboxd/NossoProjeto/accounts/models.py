from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    data_nascimento = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    foto_perfil = models.ImageField(upload_to='accounts/static/accounts/img/perfil-fotos/', blank=True, null=True)

    def __str__(self):
        return self.username
