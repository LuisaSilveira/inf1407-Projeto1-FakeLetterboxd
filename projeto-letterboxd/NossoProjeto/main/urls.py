from django.urls import path
from django.urls.conf import path
from main import views

app_name = "main"
urlpatterns = [
 path('avaliacao/', views.AvaliacaoListView.as_view(),
 name='lista-avaliacao'),
 path('avaliacao/criar/', views.AvaliacaoCreateView.as_view(),
 name='cria-avaliacao'),
 path('pessoa/criar/', views.PessoaCreateView.as_view(),
 name='cria-pessoa'),
 path('atualiza/<int:pk>/', views.AvaliacaoUpdateView.as_view(),
 name='atualiza-avaliacao'),
 path('apaga/<int:pk>/', views.AvaliacaoDeleteView.as_view(),
 name='apaga-avaliacao'),
 path('midia/', views.MidiaListView.as_view(),
 name='lista-midia'),
#  path('midias/buscar/', views.MidiaBuscaView.as_view(), 
#  name='busca-midia'),
#  path('midias/importar/', views.MidiaImportarView.as_view(), 
#  name='importar-midia'),
]