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
 path('avaliacao/<int:pk>/', views.AvaliacaoDetailView.as_view(), 
 name='detalhe-avaliacao'),

]