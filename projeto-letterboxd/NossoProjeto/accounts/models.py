from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    data_nascimento = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    foto_perfil = models.ImageField(upload_to='static/accounts/img/perfil_fotos/', default='static/accounts/img/padrao.png') #quero puxar a foto padrao.png do static/fotos 

    def __str__(self):
        return self.username
