from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from django.contrib.auth import get_user_model
from django_registration.forms import RegistrationForm
from django.utils.translation import gettext_lazy as _


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'placeholder': 'Your email address',
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'placeholder': 'Password',
                'class': 'form-control',
            }
        ),
    )


class CustomRegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = get_user_model()
