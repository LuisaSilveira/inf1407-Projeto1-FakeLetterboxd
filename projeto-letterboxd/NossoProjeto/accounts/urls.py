from accounts import views
from django.urls import path
from django.contrib.auth.views import LoginView

app_name = 'accounts'

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
]