import logging

from django.core.exceptions import ObjectDoesNotExist

from ..channel import services as channel_services
from ..user import forms as user_forms

logger = logging.getLogger(__name__)


def global_context(request):
    """Context which is applied to all views."""
    context = {}
    if request.user.is_authenticated:
        context['channels'] = channel_services.get_channels(
            user_id=request.user.id
        )
        try:
            context[
                'selected_channel'
            ] = channel_services.get_selected_channel_id(user=request.user)
        except ObjectDoesNotExist:
            context['selected_channel'] = None
    else:
        context['channels'] = []
        context['selected_channel'] = None
    context['login_form'] = user_forms.CustomAuthenticationForm(request)
    context['next'] = request.GET.get('next') or ''
    return context
