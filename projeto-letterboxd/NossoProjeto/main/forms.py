from django import forms

from main.models import Avaliacao


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
        fields = ['nota', 'comentario', 'assistido_em']
        labels = {
            'nota': 'Nota (1 a 5)',
            'comentario': 'Comentário',
        }
        help_texts = {
            'nota': 'Informe uma nota de 1 a 5.',
        }
        widgets = {
            'nota': forms.NumberInput(attrs={
                'min': '1',
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
            if nota < 1:
                raise forms.ValidationError('A nota não pode ser menor que 1.')
            if nota > 5:
                raise forms.ValidationError('A nota não pode ser maior que 5.')
        return nota