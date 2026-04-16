from django import forms

from main.models import Avaliacao, Midia


class AvaliacaoModel2Form(forms.ModelForm):
    assistido_em = forms.DateField(
        required=False,
        input_formats=['%d/%m/%Y'],
        label='Assistido em',
        help_text='Formato: DD/MM/AAAA',
        widget=forms.DateInput(attrs={
            'placeholder': 'DD/MM/AAAA',
        })
    )

    class Meta:
        model = Avaliacao
        fields = '__all__'
        labels = {
            'pessoa': 'Pessoa',
            'midia': 'Mídia',
            'nota': 'Nota (1 a 5)',
            'comentario': 'Comentário',
        }
        help_texts = {
            'nota': 'Informe uma nota de 1 a 5.',
        }
        widgets = {
            'comentario': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Escreva sua opinião sobre a mídia',
            }),
        }


class MidiaModel2Form(forms.ModelForm):
    ano_lancamento = forms.IntegerField(
        label='Ano de lançamento',
        help_text='Informe o ano com 4 dígitos.',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Ex.: 2024',
        })
    )

    class Meta:
        model = Midia
        fields = '__all__'
        labels = {
            'titulo': 'Título',
            'tipo': 'Tipo',
            'sinopse': 'Sinopse',
            'diretor': 'Diretor',
            'poster': 'Poster',
            'generos': 'Gênero',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={
                'placeholder': 'Digite o título da mídia',
            }),
            'sinopse': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Resumo da história',
            }),
            'diretor': forms.TextInput(attrs={
                'placeholder': 'Nome do diretor',
            }),
        }