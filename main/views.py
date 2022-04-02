# Create your views here.
from allauth.socialaccount.models import SocialAccount
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView, FormView, CreateView
from django.views.generic.base import ContextMixin, View

from .models import Recipe


class BaseMixin(ContextMixin, View):
    def get_context_data(self, *args, **kwargs):
        x = super().get_context_data(**kwargs)
        request = self.request
        user = request.user
        if user.is_authenticated:
            username = user.username
            if len(SocialAccount.objects.filter(user=request.user)) > 0:
                x['extra_data'] = SocialAccount.objects.filter(user=request.user)[0].extra_data
                x['avatar_url'] = SocialAccount.objects.filter(user=request.user)[0].extra_data['picture']
            else:
                x['extra_data'] = None
                x['avatar_url'] = 'static/assets/img/Default_Profile_Image.png'
        else:
            username = "Not logged in"

        x['username'] = username
        x['user'] = request.user
        return x


class IndexView(BaseMixin, TemplateView):
    template_name = 'main/index.html'


class RecipeCreateView(BaseMixin, CreateView):
    template_name = 'main/recipe.html'
    model = Recipe
    fields = ['title_text', 'ingredients_list', 'body_text']
    success_url = reverse_lazy('recipe_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)



class RecipeListView(BaseMixin, generic.ListView):
    template_name = 'main/recipeList.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        return Recipe.objects.all()
