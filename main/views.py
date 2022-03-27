# Create your views here.
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google.provider import GoogleAccount
from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, *args, **kwargs):
        x = super(Index, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            username = user.username
            if len(SocialAccount.objects.filter(user=self.request.user)) > 0:
                x['extra_data'] = SocialAccount.objects.filter(user=self.request.user)[0].extra_data
                x['avatar_url'] = SocialAccount.objects.filter(user=self.request.user)[0].extra_data['picture']
            else:
                x['extra_data'] = None
                x['avatar_url'] = 'static/assets/img/Default_Profile_Image.png'
        else:
            username = "Not logged in"

        x['username'] = username
        x['user'] = self.request.user
        return x
