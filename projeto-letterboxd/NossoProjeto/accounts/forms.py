# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUsuarioCreationForm(UserCreationForm):
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label='Data de nascimento',
        help_text='',
    )
    email = forms.EmailField(
        required=True,
        label='E-mail',
        help_text='',
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'data_nascimento')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'Nome de usuário'
        self.fields['username'].help_text = 'Máximo 150 caracteres. Letras, números e @/./+/-/_ apenas.'
        self.fields['username'].error_messages = {
            'unique': 'Esse nome de usuário já está em uso.',
        }

        self.fields['password1'].label = 'Senha'
        self.fields['password1'].help_text = (
            'A senha deve ter pelo menos 8 caracteres e não pode ser '
            'muito parecida com seus outros dados ou uma senha muito comum.'
        )

        self.fields['password2'].label = 'Confirmar senha'
        self.fields['password2'].help_text = 'Digite a mesma senha novamente para confirmação.'
