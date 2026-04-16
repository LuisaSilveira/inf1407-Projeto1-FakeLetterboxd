from django import forms

from main.models import Avaliacao, Midia, Pessoa


class PessoaModel2Form(forms.ModelForm):
    dtNasc = forms.DateField(
        input_formats=['%d/%m/%Y'],
        label='Data de nascimento',
        help_text='Formato: DD/MM/AAAA',
        widget=forms.DateInput(attrs={
            'placeholder': 'DD/MM/AAAA',
        })
    )

    class Meta:
        model = Pessoa
        fields = '__all__'
        labels = {
            'nome': 'Nome',
            'idade': 'Idade',
            'email': 'E-mail',
            'telefone': 'Telefone',
            'foto_perfil': 'Foto de perfil',
            'bio': 'Biografia',
        }
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Conte um pouco sobre você',
            }),
        }


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