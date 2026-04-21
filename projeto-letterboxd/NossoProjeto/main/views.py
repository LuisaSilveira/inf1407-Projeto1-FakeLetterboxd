from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from main.forms import AvaliacaoModel2Form, PessoaModel2Form
from main.models import Midia, Avaliacao, Pessoa

from django.shortcuts import render, get_object_or_404, redirect

from main.services.omdb_service import OMDBService
from django.contrib import messages

# Create your views here.

class AvaliacaoListView(LoginRequiredMixin, View):
    @login_required
    def get(self, request, *args, **kwargs):
        
        avaliacoes = Avaliacao.objects.all()

        # filtro de busca por título
        busca_titulo = request.GET.get('busca_titulo', '').strip()
        if busca_titulo:
            avaliacoes = avaliacoes.filter(midia__titulo__icontains=busca_titulo)
        
        # filtro do tipo de mídia (filme ou série)
        tipo_midia = request.GET.get('tipo_midia', '')
        if tipo_midia:
            avaliacoes = avaliacoes.filter(midia__tipo=tipo_midia)

        # filtro de genero da mídia
        genero_midia = request.GET.get('genero_midia', '')
        if genero_midia:
            avaliacoes = avaliacoes.filter(midia__generos=genero_midia)

        # filtro por nota (maior para menor ou menor para maior)
        ordem_nota = request.GET.get('ordem_nota', '')
        if ordem_nota == 'maior':
            avaliacoes = avaliacoes.order_by('-nota', '-dt_avaliacao')
        elif ordem_nota == 'menor':
            avaliacoes = avaliacoes.order_by('nota', '-dt_avaliacao')
        else:
            # Padrão: ordem por data (mais recente primeiro)
            avaliacoes = avaliacoes.order_by('-dt_avaliacao')
        
        contexto = {
            'avaliacoes': avaliacoes,
            'busca_titulo': busca_titulo,
            'tipo_midia': tipo_midia,
            'genero_midia': genero_midia,
            'ordem_nota': ordem_nota,
            'generos_choices': Midia.GENERO_CHOICES,

        }
 
        return render(request, 'main/listaAvaliacao.html', contexto)


class MidiaListView(LoginRequiredMixin, View):
    @login_required
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


class PessoaCreateView(LoginRequiredMixin, View):
    @login_required
    def get(self, request):
        contexto = {
            'formulario': PessoaModel2Form(),
        }
        return render(request, 'main/formulario.html', contexto)

    @login_required
    def post(self, request, *args, **kwargs):
        formulario = PessoaModel2Form(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect(reverse_lazy('portal:home'))

        contexto = {
            'formulario': formulario,
        }
        return render(request, 'main/formulario.html', contexto)


class AvaliacaoCreateView(LoginRequiredMixin, View):
    @login_required
    def get(self, request):
        termo_busca = request.GET.get('busca_midia', '')
        midias_encontradas = []
        midia_selecionada_id = request.GET.get('midia_selecionada')
        midia_selecionada = None
        
        # Se tem termo de busca, busca na API
        if termo_busca:
            midias_encontradas = OMDBService.buscar_multiplos(termo_busca)
        
        # Se tem mídia selecionada, busca/cria no banco
        if midia_selecionada_id:
            midia_selecionada = Midia.objects.filter(imdb_id=midia_selecionada_id).first()
            
            if not midia_selecionada:
                # Busca na API e cria
                dados = OMDBService.buscar_por_imdb_id(midia_selecionada_id)
                if dados:
                    midia_selecionada = Midia.objects.create(
                        titulo=dados['titulo'],
                        tipo=dados['tipo'],
                        sinopse=dados['sinopse'],
                        ano_lancamento=dados['ano_lancamento'],
                        diretor=dados['diretor'],
                        generos=dados['generos'],
                        imdb_id=dados['imdb_id'],
                        poster_url=dados['poster_url'],
                    )

            trocar_midia = False
        
        contexto = {
            'formulario': AvaliacaoModel2Form(),
            'termo_busca': termo_busca,
            'midias_encontradas': midias_encontradas,
            'midia_selecionada': midia_selecionada,
        }
        return render(request, 'main/criaAvaliacao.html', contexto)

    @login_required
    def post(self, request):
        formulario = AvaliacaoModel2Form(request.POST)
        midia_id = request.POST.get('midia_id')
        
        if formulario.is_valid() and midia_id:
            try:
                midia = Midia.objects.get(id=midia_id)
                avaliacao = formulario.save(commit=False)
                avaliacao.midia = midia
                avaliacao.save()
                return HttpResponseRedirect(reverse_lazy('main:lista-avaliacao'))
            except Midia.DoesNotExist:
                messages.error(request, 'Mídia não encontrada')
        else:
            if not midia_id:
                messages.error(request, 'Por favor, selecione uma mídia')
        
        contexto = {
            'formulario': formulario,
        }
        return render(request, 'main/criaAvaliacao.html', contexto)

class AvaliacaoUpdateView(LoginRequiredMixin, View):
    @login_required
    def get(self, request, pk, *args, **kwargs):
        avaliacao = get_object_or_404(Avaliacao, pk=pk)
        formulario = AvaliacaoModel2Form(instance=avaliacao)

        termo_busca = request.GET.get('busca_midia', '')
        trocar_midia = request.GET.get('trocar_midia') == '1'
        midias_encontradas = []
        midia_selecionada = avaliacao.midia
        midia_selecionada_id = request.GET.get('midia_selecionada')

        if termo_busca:
            midias_encontradas = OMDBService.buscar_multiplos(termo_busca)

        if midia_selecionada_id:
            midia_selecionada = Midia.objects.filter(imdb_id=midia_selecionada_id).first()

            if not midia_selecionada:
                dados = OMDBService.buscar_por_imdb_id(midia_selecionada_id)
                if dados:
                    midia_selecionada = Midia.objects.create(
                        titulo=dados['titulo'],
                        tipo=dados['tipo'],
                        sinopse=dados['sinopse'],
                        ano_lancamento=dados['ano_lancamento'],
                        diretor=dados['diretor'],
                        generos=dados['generos'],
                        imdb_id=dados['imdb_id'],
                        poster_url=dados['poster_url'],
                    )

        contexto = {
            'avaliacao': formulario,
            'avaliacao_obj': avaliacao,
            'termo_busca': termo_busca,
            'trocar_midia': trocar_midia,
            'midias_encontradas': midias_encontradas,
            'midia_selecionada': midia_selecionada,
        }
        return render(request, 'main/atualizaAvaliacao.html', contexto)

    @login_required
    def post(self, request, pk, *args, **kwargs):
        avaliacao = get_object_or_404(Avaliacao, pk=pk)
        formulario = AvaliacaoModel2Form(request.POST, instance=avaliacao)
        midia_id = request.POST.get('midia_id')

        if formulario.is_valid():
            avaliacao_editada = formulario.save(commit=False)

            if midia_id:
                try:
                    avaliacao_editada.midia = Midia.objects.get(id=midia_id)
                except Midia.DoesNotExist:
                    messages.error(request, 'Mídia selecionada não encontrada')
                    contexto = {
                        'avaliacao': formulario,
                        'avaliacao_obj': avaliacao,
                        'midia_selecionada': avaliacao.midia,
                        'termo_busca': '',
                        'trocar_midia': False,
                        'midias_encontradas': [],
                    }
                    return render(request, 'main/atualizaAvaliacao.html', contexto)

            avaliacao_editada.save()
            return HttpResponseRedirect(reverse_lazy("main:lista-avaliacao"))
        else:
            contexto = {
                'avaliacao': formulario,
                'avaliacao_obj': avaliacao,
                'midia_selecionada': avaliacao.midia,
                'termo_busca': '',
                'trocar_midia': False,
                'midias_encontradas': [],
            }
            return render(request, 'main/atualizaAvaliacao.html', contexto)

class AvaliacaoDeleteView(LoginRequiredMixin, View):
    @login_required
    def get(self, request, pk, *args, **kwargs):
        avaliacao = Avaliacao.objects.get(pk=pk)
        contexto = { 'avaliacao': avaliacao, }
        return render(request, 'main/apagaAvaliacao.html', contexto)
    @login_required
    def post(self, request, pk, *args, **kwargs):
        avaliacao = Avaliacao.objects.get(pk=pk)
        avaliacao.delete()
        return HttpResponseRedirect(reverse_lazy("main:lista-avaliacao"))


# class MidiaBuscaView(View):
#     """View para buscar mídias na API OMDB"""
#     def get(self, request):
#         termo = request.GET.get('q', '')
#         resultados = []
        
#         if termo:
#             resultados = OMDBService.buscar_multiplos(termo)
        
#         contexto = {
#             'termo': termo,
#             'resultados': resultados,
#         }
#         return render(request, 'main/buscaMidia.html', contexto)

# class MidiaImportarView(View):
#     """View para importar uma mídia da OMDB para o banco"""
#     def post(self, request):
#         imdb_id = request.POST.get('imdb_id')
        
#         if not imdb_id:
#             messages.error(request, 'ID do IMDB não fornecido')
#             return HttpResponseRedirect(reverse_lazy('main:busca-midia'))
        
#         # Verifica se já existe
#         if Midia.objects.filter(imdb_id=imdb_id).exists():
#             messages.warning(request, 'Esta mídia já está cadastrada')
#             return HttpResponseRedirect(reverse_lazy('main:lista-midia'))
        
#         # Busca dados da API
#         dados = OMDBService.buscar_por_imdb_id(imdb_id)
        
#         if dados:
#             # Cria a mídia
#             midia = Midia.objects.create(
#                 titulo=dados['titulo'],
#                 tipo=dados['tipo'],
#                 sinopse=dados['sinopse'],
#                 ano_lancamento=dados['ano_lancamento'],
#                 diretor=dados['diretor'],
#                 generos=dados['generos'],
#                 imdb_id=dados['imdb_id'],
#                 poster_url=dados['poster_url'],
#             )
#             messages.success(request, f'Mídia "{midia.titulo}" importada com sucesso!')
#         else:
#             messages.error(request, 'Erro ao buscar dados da mídia')
        
#         return HttpResponseRedirect(reverse_lazy('main:lista-midia'))