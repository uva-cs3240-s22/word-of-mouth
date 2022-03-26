from django.shortcuts import render
from datetime import datetime
# Create your views here.
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Recipe, RecipeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic


class Index(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self,*args, **kwargs):
        return {"user": self.request.user}


def recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('')
    else:
        form = RecipeForm()
    return render(request, 'main/recipe.html', {'form':form})

class RecipeList(generic.ListView):
    template_name = 'main/recipeList.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        return Recipe.objects.all()