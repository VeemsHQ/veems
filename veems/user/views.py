from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.shortcuts import render, redirect


class Email(forms.EmailField):
    def clean(self, value):
        super(Email, self).clean(value)
        try:
            get_user_model().objects.get(email=value)
            raise forms.ValidationError(
                "This email is already registered. Use the 'forgot password' "
                'link on the login page'
            )
        except get_user_model().DoesNotExist:
            return value


class CustomUserCreationForm(UserCreationForm):
    email = Email()

    class Meta:
        model = get_user_model()
        fields = ('email',)


def signup(request):
    # TODO: test
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            assert user
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
