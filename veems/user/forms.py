from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
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


class UserEmailField(forms.EmailField):
    def clean(self, value):
        super().clean(value)
        try:
            get_user_model().objects.get(email=value)
            raise forms.ValidationError(
                "This email is already registered. Use the 'forgot password' "
                'link on the login page'
            )
        except get_user_model().DoesNotExist:
            return value


class CustomUserCreationForm(UserCreationForm):
    email = UserEmailField()
    sync_videos_interested = forms.BooleanField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('email', 'sync_videos_interested')
