from django.shortcuts import render
#trocar depois
from main.models import Pessoa, Midia, Avaliacao
#from account.models import Pessoa
from django.views.generic.base import View

# Create your views here.

class AvaliacaoListView(View):
    def get(self, request, *args, **kwargs):
            avaliacoes = Avaliacao.objects.all()

            contexto = {
                'avaliacoes': avaliacoes
            }

            return render(
                request,
                'main/listaAvaliacao.html',
                contexto
            )


class MidiaListView(View):
    def get(self, request, *args, **kwargs):
        midias = Midia.objects.all()

        contexto = {
            'midias': midias
        }

        return render(
            request,
            'main/listaMidia.html',
            contexto
        )