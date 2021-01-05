from django.contrib.auth import login
from django_registration.signals import user_activated


def login_on_activation(sender, user, request, **kwargs):
    """Auto-login the user after activate their email address."""
    login(request, user)


user_activated.connect(login_on_activation)
