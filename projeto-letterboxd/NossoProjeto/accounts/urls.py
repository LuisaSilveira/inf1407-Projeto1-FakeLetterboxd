from accounts import views
from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from accounts.views import MeuUpdateView
from accounts.models import CustomUser
from accounts.forms import CustomSetPasswordForm


app_name = 'accounts'

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/update/<int:pk>/', MeuUpdateView.as_view(template_name='accounts/perfil_update.html',
                                                          success_url=reverse_lazy('accounts:perfil'),
                                                          model = CustomUser), name='perfil-update'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='portal:home'), name='logout'),
    path('password_reset/', PasswordResetView.as_view(template_name='accounts/password_reset_form.html',
                                                    success_url=reverse_lazy('accounts:password_reset_sent'),
                                                    email_template_name='accounts/password_reset_email_txt.html',
                                                    html_email_template_name='accounts/password_reset_email.html',
                                                    subject_template_name='accounts/password_reset_subject.txt',
                                                    from_email = 'rafaribeiro2013@gmail.com'), name='password_reset'),
    path('password_reset_sent/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), name='password_reset_sent'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html', form_class=CustomSetPasswordForm, success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]