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
        input_formats=['%Y-%m-%d'],
        label='Assistido em',
        widget=forms.DateInput(attrs={
            'type': 'date',
        })
    )
 
    class Meta:
        model = Avaliacao
        fields = ['pessoa', 'nota', 'comentario', 'assistido_em']
        labels = {
            'pessoa': 'Pessoa',
            'nota': 'Nota (0 a 5)',
            'comentario': 'Comentário',
        }
        help_texts = {
            'nota': 'Informe uma nota de 0 a 5.',
        }
        widgets = {
            'nota': forms.NumberInput(attrs={
                'min': '0',
                'max': '5',
                'step': '1',
            }),
            'comentario': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Escreva sua opinião sobre a mídia',
            }),
        }
 
    def clean_nota(self):
        nota = self.cleaned_data.get('nota')
        if nota is not None:
            if nota < 0:
                raise forms.ValidationError('A nota não pode ser negativa.')
            if nota > 5:
                raise forms.ValidationError('A nota não pode ser maior que 5.')
        return nota