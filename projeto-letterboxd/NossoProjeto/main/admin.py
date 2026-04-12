from django.contrib import admin

# Register your models here.
from main.models import Pessoa,Midia,Avaliacao
admin.site.register(Pessoa)
admin.site.register(Midia)
admin.site.register(Avaliacao)