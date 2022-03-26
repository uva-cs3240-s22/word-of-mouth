from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('recipe/', views.recipe, name='recipe'),
    path('recipe/list', views.RecipeList.as_view(), name='recipe_list')
]