import unicodedata

from django import forms
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
from django.contrib.auth.models import User
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import UsernameField

UserModel = get_user_model()

class AuthenticationForm(auth_forms.AuthenticationForm):

    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'type': 'text', 'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'type': 'password', 'class': 'form-control', 'placeholder': 'Password'}),
    )


class UserCreationForm(auth_forms.UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Username'}))

    email = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'email'}))

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'type': 'password', 'class': 'form-control', 'placeholder': 'Password'}),
        help_text=password_validation.password_validators_help_text_html(),
        )
       
    password2 = forms.CharField(
        label=_("Password confirmation"),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'type': 'password', 'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        field_classes = {'username': UsernameField}


class PasswordResetForm(auth_forms.PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control', 'placeholder': 'Your Email'})
    )


class SetPasswordForm(auth_forms.SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'New Password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Confirm New Password'}),
    )