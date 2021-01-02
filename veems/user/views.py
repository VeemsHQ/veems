import logging

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import logout as logout_

from . import forms

logger = logging.getLogger(__name__)


def signup(request):
    if request.method == 'POST':
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            logger.info('Signed up new user %s', username)
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            next_url = (
                request.GET.get('next')
                or settings.DEFAULT_POST_SIGNUP_REDIRECT_VIEW_NAME
            )
            return redirect(next_url)
        else:
            logger.warning('User signup attempt failed: %s', form.errors)
    else:
        form = forms.CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def logout(request):
    logout_(request)
    return redirect(settings.DEFAULT_POST_LOGOUT_REDIRECT_VIEW_NAME)
