# Create your views here.
from allauth.socialaccount.models import SocialAccount
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import TemplateView, CreateView
from django.views.generic.base import ContextMixin, View
from django.db.models import Q
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView

from .models import Recipe, CommentForm


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

        x['username'] = user.socialaccount_set.first().extra_data['name']
        x['user'] = request.user
        return x


# https://docs.djangoproject.com/en/4.0/topics/class-based-views/mixins/
# partially yoinked from here
# class CommentMixin(FormMixin, View):
#     model = Comment
#     form_class = CommentForm
#
#     def get_success_url(self):
#         return self.request.get_full_path()
#
#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden()
#         # self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#     def form_valid(self, form):
#         # Here, we would record the user's interest using the message
#         # passed in form.cleaned_data['message']
#         form.instance.owner = self.request.user
#         form.instance.recipe = self.get_object()
#         return super().form_valid(form)


class IndexView(BaseMixin, TemplateView):
    template_name = 'main/index.html'


class RecipeCreateView(BaseMixin, CreateView):
    template_name = 'main/recipe.html'
    model = Recipe
    fields = ['title_text', 'ingredients_list', 'body_text', 'picture']
    success_url = reverse_lazy('recipe_list')

    def get_initial(self):
        if 'from' in self.request.GET:
            return model_to_dict(Recipe.objects.get(id=self.request.GET['from']), fields=self.fields)
        else:
            return self.initial

    def form_valid(self, form):
        if 'from' in self.request.POST:
            form.instance.parent = Recipe.objects.get(id=self.request.POST['from'])
        elif 'from' in self.request.GET:
            form.instance.parent = Recipe.objects.get(id=self.request.GET['from'])

        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipeListView(BaseMixin, generic.ListView):
    template_name = 'main/recipeList.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        return Recipe.objects.all()


class RecipeCommentFormView(SingleObjectMixin, FormView):
    template_name = 'main/recipe_detail.html'
    form_class = CommentForm
    model = Recipe

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        form.instance.owner = self.request.user
        form.instance.recipe = self.object
        form.save()
        return super().form_valid(form)


class RecipeView(View):

    def get(self, request, *args, **kwargs):
        view = RecipeDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = RecipeCommentFormView.as_view()
        return view(request, *args, **kwargs)


class RecipeDetailView(BaseMixin, generic.DetailView):
    template_name = 'main/recipe_detail.html'
    model = Recipe
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


def favorite_add(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if recipe.favorites.filter(id=request.user.id).exists():
        recipe.favorites.remove(request.user)
    else:
        recipe.favorites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class FavoriteListView(BaseMixin, generic.ListView):
    template_name = 'main/favorites.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        request = self.request
        return Recipe.objects.filter(favorites=request.user)

class SearchResultsView(BaseMixin, generic.ListView):
    model = Recipe
    template_name = 'main/search_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get("query")
        return Recipe.objects.filter(
            Q(title_text__icontains=query) | Q(ingredients_list__icontains=query) | Q(body_text__icontains=query)
        )
