# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUsuarioCreationForm(UserCreationForm):
    # Definir widget de data para ficar mais amigável no HTML (opcional)
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        required=False
    )
    email = forms.EmailField(required=True) # Caso queira tornar o email obrigatório também

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'data_nascimento')