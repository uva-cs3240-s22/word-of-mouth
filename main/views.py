# Create your views here.
from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self,*args, **kwargs):
        username = self.request.user.username if self.request.user.is_authenticated else "Not logged in"
        x = super(Index, self).get_context_data(**kwargs)
        x['user'] = self.request.user
        x['username'] = username
        return x
