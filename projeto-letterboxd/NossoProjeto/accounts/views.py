from django.shortcuts import render
from django.shortcuts import redirect
from .forms import CustomUsuarioCreationForm

def cadastro(request):
    if request.method == 'POST':
        formulario = CustomUsuarioCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('home')
    else:
        formulario = CustomUsuarioCreationForm()
    contexto = {'form': formulario, }
    return render(request,'accounts/cadastro.html', contexto)