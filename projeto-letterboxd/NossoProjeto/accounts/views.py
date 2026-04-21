from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUsuarioCreationForm

@login_required(login_url='accounts:login')
def perfil(request):
    return render(request, 'accounts/perfil.html')

def cadastro(request):
    if request.method == 'POST':
        formulario = CustomUsuarioCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('main:lista-avaliacao')
    else:
        formulario = CustomUsuarioCreationForm()
    contexto = {'form': formulario, }
    return render(request,'accounts/cadastro.html', contexto)