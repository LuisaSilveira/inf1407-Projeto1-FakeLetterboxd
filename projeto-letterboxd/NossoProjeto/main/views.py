from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from django.contrib.auth import get_user_model
from main.forms import AvaliacaoModel2Form
from main.models import Midia, Avaliacao
from main.services.omdb_service import OMDBService
from django.contrib import messages


class AvaliacaoListView(LoginRequiredMixin, View):
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

        #filtro de busca por pessoa/usuário
        busca_pessoa = request.GET.get('busca_pessoa', '').strip()
        if busca_pessoa:
            avaliacoes = avaliacoes.filter(pessoa__username__icontains=busca_pessoa)

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
            'busca_pessoa': busca_pessoa,
            'generos_choices': Midia.GENERO_CHOICES,
        }
 
        return render(request, 'main/listaAvaliacao.html', contexto)



class AvaliacaoCreateView(LoginRequiredMixin, View):
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
                        # Novos campos
                        duracao=dados.get('duracao', ''),
                        idioma=dados.get('idioma', ''),
                        pais=dados.get('pais', ''),
                        elenco=dados.get('elenco', ''),
                        num_temporadas=dados.get('num_temporadas'),
                        classificacao=dados.get('classificacao', ''),
                    )
        
        contexto = {
            'formulario': AvaliacaoModel2Form(),
            'termo_busca': termo_busca,
            'midias_encontradas': midias_encontradas,
            'midia_selecionada': midia_selecionada,
        }
        return render(request, 'main/criaAvaliacao.html', contexto)

    def post(self, request):
        formulario = AvaliacaoModel2Form(request.POST)
        midia_id = request.POST.get('midia_id')
        
        if formulario.is_valid() and midia_id:
            try:
                midia = Midia.objects.get(id=midia_id)
                avaliacao = formulario.save(commit=False)
                avaliacao.midia = midia
                avaliacao.pessoa = request.user
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
    def get(self, request, pk, *args, **kwargs):
        avaliacao = get_object_or_404(Avaliacao, pk=pk)
        if avaliacao.pessoa != request.user:
            raise PermissionDenied
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
                        # Novos campos
                        duracao=dados.get('duracao', ''),
                        idioma=dados.get('idioma', ''),
                        pais=dados.get('pais', ''),
                        elenco=dados.get('elenco', ''),
                        num_temporadas=dados.get('num_temporadas'),
                        classificacao=dados.get('classificacao', ''),
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

    def post(self, request, pk, *args, **kwargs):
        avaliacao = get_object_or_404(Avaliacao, pk=pk)
        if avaliacao.pessoa != request.user:
            raise PermissionDenied
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

            avaliacao_editada.pessoa = request.user
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
    def get(self, request, pk, *args, **kwargs):
        avaliacao = get_object_or_404(Avaliacao, pk=pk)
        if avaliacao.pessoa != request.user:
            raise PermissionDenied
        contexto = { 'avaliacao': avaliacao, }
        return render(request, 'main/apagaAvaliacao.html', contexto)
    
    def post(self, request, pk, *args, **kwargs):
        avaliacao = get_object_or_404(Avaliacao, pk=pk)
        if avaliacao.pessoa != request.user:
            raise PermissionDenied
        avaliacao.delete()
        return HttpResponseRedirect(reverse_lazy("main:lista-avaliacao"))


class AvaliacaoDetailView(LoginRequiredMixin, View):
    """View para exibir detalhes completos de uma avaliação"""
    def get(self, request, pk, *args, **kwargs):
        avaliacao = get_object_or_404(Avaliacao, pk=pk)
        
        contexto = {
            'avaliacao': avaliacao,
        }
        return render(request, 'main/detalheAvaliacao.html', contexto)


class PessoaProfileView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        pessoa = get_object_or_404(get_user_model(), pk=pk)

        avaliacoes = pessoa.avaliacoes.select_related('midia')

        busca_titulo = request.GET.get('busca_titulo', '').strip()
        if busca_titulo:
            avaliacoes = avaliacoes.filter(midia__titulo__icontains=busca_titulo)

        tipo_midia = request.GET.get('tipo_midia', '')
        if tipo_midia:
            avaliacoes = avaliacoes.filter(midia__tipo=tipo_midia)

        genero_midia = request.GET.get('genero_midia', '')
        if genero_midia:
            avaliacoes = avaliacoes.filter(midia__generos=genero_midia)

        ordem_nota = request.GET.get('ordem_nota', '')
        if ordem_nota == 'maior':
            avaliacoes = avaliacoes.order_by('-nota', '-dt_avaliacao')
        elif ordem_nota == 'menor':
            avaliacoes = avaliacoes.order_by('nota', '-dt_avaliacao')
        else:
            avaliacoes = avaliacoes.order_by('-dt_avaliacao')

        contexto = {
            'pessoa': pessoa,
            'avaliacoes': avaliacoes,
            'busca_titulo': busca_titulo,
            'tipo_midia': tipo_midia,
            'genero_midia': genero_midia,
            'ordem_nota': ordem_nota,
            'generos_choices': Midia.GENERO_CHOICES,
        }
        return render(request, 'main/perfil.html', contexto)
