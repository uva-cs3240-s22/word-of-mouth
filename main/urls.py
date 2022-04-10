from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('recipe/add', views.RecipeCreateView.as_view(), name='new_recipe'),
    path('recipe/list', views.RecipeListView.as_view(), name='recipe_list'),
    path('recipe/fav/<int:id>/', views.favorite_add, name='favorite_add'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorites_list')
]