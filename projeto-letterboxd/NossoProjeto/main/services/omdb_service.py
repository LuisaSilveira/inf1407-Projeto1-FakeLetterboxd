import requests
from decouple import config
from typing import Optional, Dict, List

class OMDBService:
    BASE_URL = 'http://www.omdbapi.com/'
    API_KEY = config('OMDB_API_KEY')
    
    GENERO_MAP = {
        'Action': 'acao',
        'Comedy': 'comedia',
        'Horror': 'terror',
        'Romance': 'romance',
        'Drama': 'drama',
        'Sci-Fi': 'ficcao',
        'Adventure': 'aventura',
        'Thriller': 'suspense',
        'Animation': 'animacao',
        'Documentary': 'documentario',
    }
    
    @classmethod
    def buscar_por_titulo(cls, titulo: str) -> Optional[Dict]:
        """Busca uma mídia específica por título"""
        params = {
            'apikey': cls.API_KEY,
            't': titulo,
        }
        
        response = requests.get(cls.BASE_URL, params=params)
        data = response.json()
        
        if data.get('Response') == 'True':
            return cls._formatar_dados(data)
        return None
    
    @classmethod
    def buscar_multiplos(cls, termo: str) -> List[Dict]:
        """Busca múltiplas mídias por termo de pesquisa"""
        params = {
            'apikey': cls.API_KEY,
            's': termo,
        }
        
        response = requests.get(cls.BASE_URL, params=params)
        data = response.json()
        
        if data.get('Response') == 'True':
            resultados = []
            for item in data.get('Search', []):
                # Busca detalhes completos de cada resultado
                detalhes = cls.buscar_por_titulo(item['Title'])
                if detalhes:
                    resultados.append(detalhes)
            return resultados
        return []
    
    @classmethod
    def buscar_por_imdb_id(cls, imdb_id: str) -> Optional[Dict]:
        """Busca uma mídia por ID do IMDB"""
        params = {
            'apikey': cls.API_KEY,
            'i': imdb_id,
        }
        
        response = requests.get(cls.BASE_URL, params=params)
        data = response.json()
        
        if data.get('Response') == 'True':
            return cls._formatar_dados(data)
        return None
    
    @classmethod
    def _formatar_dados(cls, data: Dict) -> Dict:
        """Formata os dados da API OMDB para o formato do modelo"""
        # Mapeia tipo
        tipo = 'filme' if data.get('Type') == 'movie' else 'serie'
        
        # Mapeia gênero (pega o primeiro gênero listado)
        generos_api = data.get('Genre', '').split(', ')
        genero = 'drama'  # padrão
        for g in generos_api:
            if g in cls.GENERO_MAP:
                genero = cls.GENERO_MAP[g]
                break
        
        # Trata ano (pode vir como "2020" ou "2020-2024" para séries)
        ano = data.get('Year', '').split('–')[0].split('-')[0]
        try:
            ano_lancamento = int(ano)
        except ValueError:
            ano_lancamento = 2000
        
        return {
            'titulo': data.get('Title', ''),
            'tipo': tipo,
            'sinopse': data.get('Plot', ''),
            'ano_lancamento': ano_lancamento,
            'diretor': data.get('Director', ''),
            'generos': genero,
            'poster_url': data.get('Poster', ''),
            'imdb_id': data.get('imdbID', ''),
        }