from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import views
from django.contrib import messages
from django.shortcuts import redirect
from .forms import AuthenticationForm
from django.urls import reverse
# Create your views here.

class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/signup.html'
    
    def get_success_url(self):
        return reverse('login')

class LoginView(views.LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    form_class = AuthenticationForm

    def get_success_url(self):
        return reverse('home')

class LogoutView(views.LogoutView):
    template_name = 'accounts/logged_out.html'


class PasswordResetView(views.PasswordResetView):
    form_class = PasswordResetForm
    from_email = 'nuwanjithm@gmail.com'
    html_email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    template_name = 'accounts/password_reset_form.html'

class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = SetPasswordForm

class PasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'