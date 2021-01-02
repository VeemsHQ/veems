from ..channel import services as channel_services
from ..user import forms as user_forms


def global_context(request):
    """Context which is applied to all views."""
    context = {}
    context['channels'] = channel_services.get_channels(
        user_id=request.user.id
    )
    context['login_form'] = user_forms.CustomAuthenticationForm(request)
    context['next'] = request.GET.get('next') or ''
    return context
