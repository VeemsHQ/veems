from django.views.generic import TemplateView

from ..common.views import GlobalContextMixin


class IndexView(GlobalContextMixin, TemplateView):
    template_name = 'home/index.html'
