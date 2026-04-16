from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.views.generic.base import View

from main.forms import AvaliacaoModel2Form, MidiaModel2Form
from main.models import Midia, Avaliacao, Pessoa

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


class AvaliacaoCreateView(View):
    def get(self, request, *args, **kwargs):
        contexto = {
            'formulario': AvaliacaoModel2Form(),
            'titulo': 'Cadastrar avaliação',
            'botao': 'Salvar avaliação',
        }
        return render(request, 'main/formulario.html', contexto)

    def post(self, request, *args, **kwargs):
        formulario = AvaliacaoModel2Form(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect(reverse_lazy('main:lista-avaliacao'))

        contexto = {
            'formulario': formulario,
            'titulo': 'Cadastrar avaliação',
            'botao': 'Salvar avaliação',
        }
        return render(request, 'main/formulario.html', contexto)


class MidiaCreateView(View):
    def get(self, request, *args, **kwargs):
        contexto = {
            'formulario': MidiaModel2Form(),
            'titulo': 'Cadastrar mídia',
            'botao': 'Salvar mídia',
        }
        return render(request, 'main/formulario.html', contexto)

    def post(self, request, *args, **kwargs):
        formulario = MidiaModel2Form(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect(reverse_lazy('main:lista-midia'))

        contexto = {
            'formulario': formulario,
            'titulo': 'Cadastrar mídia',
            'botao': 'Salvar mídia',
        }
        return render(request, 'main/formulario.html', contexto)