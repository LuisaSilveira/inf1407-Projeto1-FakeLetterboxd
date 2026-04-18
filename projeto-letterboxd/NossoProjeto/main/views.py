from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.views.generic.base import View

from main.forms import AvaliacaoModel2Form, PessoaModel2Form
from main.models import Midia, Avaliacao, Pessoa

from django.shortcuts import render, get_object_or_404

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


class PessoaCreateView(View):
    def get(self, request):
        contexto = {
            'formulario': PessoaModel2Form(),
        }
        return render(request, 'main/formulario.html', contexto)

    def post(self, request, *args, **kwargs):
        formulario = PessoaModel2Form(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect(reverse_lazy('portal:home'))

        contexto = {
            'formulario': formulario,
        }
        return render(request, 'main/formulario.html', contexto)


class AvaliacaoCreateView(View):
    def get(self, request):
        contexto = {
            'formulario': AvaliacaoModel2Form(),
        }
        return render(request, 'main/criaAvaliacao.html', contexto)

    def post(self, request):
        formulario = AvaliacaoModel2Form(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect(reverse_lazy('main:lista-avaliacao'))

        contexto = {
            'formulario': formulario,
        }
        return render(request, 'main/criaAvaliacao.html', contexto)

class AvaliacaoUpdateView(View):
    def get(self, request, pk, *args, **kwargs):
        avaliacao = Avaliacao.objects.get(pk=pk)
        formulario = AvaliacaoModel2Form(instance=avaliacao)
        contexto = {'avaliacao': formulario, }
        return render(request, 'main/atualizaAvaliacao.html', contexto)

    def post(self, request, pk, *args, **kwargs):
        avaliacao = get_object_or_404(Avaliacao, pk=pk)
        formulario = AvaliacaoModel2Form(request.POST, instance=avaliacao)
        if formulario.is_valid():
            avaliacao = formulario.save() # cria uma avaliacao com os dados do formulário
            avaliacao.save() # salva uma avaliacao no banco de dados
            return HttpResponseRedirect(reverse_lazy("main:lista-avaliacao"))
        else:
            contexto = {'avaliacao': formulario, }
            return render(request, 'main/atualizaAvaliacao.html', contexto)

class AvaliacaoDeleteView(View):
    def get(self, request, pk, *args, **kwargs):
        avaliacao = Avaliacao.objects.get(pk=pk)
        contexto = { 'avaliacao': avaliacao, }
        return render(request, 'main/apagaAvaliacao.html', contexto)
    def post(self, request, pk, *args, **kwargs):
        avaliacao = Avaliacao.objects.get(pk=pk)
        avaliacao.delete()
        return HttpResponseRedirect(reverse_lazy("main:lista-avaliacao"))