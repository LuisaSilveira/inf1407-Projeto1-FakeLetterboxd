from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUsuarioCreationForm, CustomUserUpdateForm
from django.views.generic.edit import UpdateView

@login_required(login_url='accounts:login')
def perfil(request):
    avaliacoes = request.user.avaliacoes.select_related('midia').order_by('-dt_avaliacao')
    return render(request, 'accounts/perfil.html', {'avaliacoes': avaliacoes})

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


class MeuUpdateView(UpdateView):
    form_class = CustomUserUpdateForm

    def get(self, request, pk, *args, **kwargs):
        if request.user.id == pk:
            return super().get(request, pk, *args, **kwargs)
        else:
            return redirect('main:lista-avaliacao')