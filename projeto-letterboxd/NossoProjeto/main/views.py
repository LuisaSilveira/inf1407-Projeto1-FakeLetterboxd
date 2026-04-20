from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.views.generic.base import View

from main.forms import AvaliacaoModel2Form, PessoaModel2Form
from main.models import Midia, Avaliacao, Pessoa

from django.shortcuts import render, get_object_or_404

from main.services.omdb_service import OMDBService
from django.contrib import messages

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


class MidiaBuscaView(View):
    """View para buscar mídias na API OMDB"""
    def get(self, request):
        termo = request.GET.get('q', '')
        resultados = []
        
        if termo:
            resultados = OMDBService.buscar_multiplos(termo)
        
        contexto = {
            'termo': termo,
            'resultados': resultados,
        }
        return render(request, 'main/buscaMidia.html', contexto)

class MidiaImportarView(View):
    """View para importar uma mídia da OMDB para o banco"""
    def post(self, request):
        imdb_id = request.POST.get('imdb_id')
        
        if not imdb_id:
            messages.error(request, 'ID do IMDB não fornecido')
            return HttpResponseRedirect(reverse_lazy('main:busca-midia'))
        
        # Verifica se já existe
        if Midia.objects.filter(imdb_id=imdb_id).exists():
            messages.warning(request, 'Esta mídia já está cadastrada')
            return HttpResponseRedirect(reverse_lazy('main:lista-midia'))
        
        # Busca dados da API
        dados = OMDBService.buscar_por_imdb_id(imdb_id)
        
        if dados:
            # Cria a mídia
            midia = Midia.objects.create(
                titulo=dados['titulo'],
                tipo=dados['tipo'],
                sinopse=dados['sinopse'],
                ano_lancamento=dados['ano_lancamento'],
                diretor=dados['diretor'],
                generos=dados['generos'],
                imdb_id=dados['imdb_id'],
                poster_url=dados['poster_url'],
            )
            messages.success(request, f'Mídia "{midia.titulo}" importada com sucesso!')
        else:
            messages.error(request, 'Erro ao buscar dados da mídia')
        
        return HttpResponseRedirect(reverse_lazy('main:lista-midia'))