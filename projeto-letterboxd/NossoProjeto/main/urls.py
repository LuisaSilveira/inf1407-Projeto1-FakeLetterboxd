from django.urls import path
from django.urls.conf import path
from main import views

app_name = "main"
urlpatterns = [
 path('avaliacao/', views.AvaliacaoListView.as_view(),
 name='lista-avaliacao'),
 path('avaliacao/criar/', views.AvaliacaoCreateView.as_view(),
 name='cria-avaliacao'),
 path('midia/', views.MidiaListView.as_view(),
 name='lista-midia'),
 path('midia/criar/', views.MidiaCreateView.as_view(),
 name='cria-midia'),
]