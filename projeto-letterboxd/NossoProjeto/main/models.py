from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Pessoa(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(
    max_length=100, help_text='Entre o nome')
    idade = models.IntegerField(help_text='Entre a idade')
    email = models.EmailField(
    help_text='Informe o email', max_length=254)
    telefone = models.CharField(
    help_text='Telefone com DDD e DDI', max_length=20)
    dtNasc = models.DateField(
    help_text='Nascimento no formato DD/MM/AAAA',
    verbose_name='Data de nascimento')
    foto_perfil = models.ImageField(upload_to='perfis/', null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.nome

class Midia(models.Model):
    TIPO_CHOICES = [
        ('filme', 'Filme'),
        ('serie', 'Série'),
    ]

    GENERO_CHOICES = [
        ('acao', 'Ação'),
        ('comedia', 'Comédia'),
        ('terror', 'Terror'),
        ('romance', 'Romance'),
        ('drama', 'Drama'),
        ('ficcao', 'Ficção Científica'),
        ('aventura', 'Aventura'),
        ('suspense', 'Suspense'),
        ('animacao', 'Animação'),
        ('documentario', 'Documentário'),
    ]

    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    sinopse = models.TextField(blank=True)
    ano_lancamento = models.IntegerField()
    diretor = models.CharField(max_length=100, blank=True)
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    generos = models.CharField(max_length=50, choices=GENERO_CHOICES)

    def __str__(self):
        return f'{self.titulo} ({self.ano_lancamento})'

class Avaliacao(models.Model):
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='avaliacoes')
    midia = models.ForeignKey(Midia, on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.TextField(blank=True)
    dt_avaliacao = models.DateTimeField(auto_now_add=True)
    dt_atualizacao = models.DateTimeField(auto_now=True)
    assistido_em = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.pessoa.nome} → {self.midia.titulo}: {self.nota}★'