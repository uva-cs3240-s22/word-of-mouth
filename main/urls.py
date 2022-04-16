from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('recipe/add', views.RecipeCreateView.as_view(), name='new_recipe'),
    path('recipe/list', views.RecipeListView.as_view(), name='recipe_list'),
    path('recipe/fav/<int:id>', views.favorite_add, name='favorite_add'),
    path('recipe/<int:pk>', views.RecipeView.as_view(), name='recipe_detail'),
    path('favorites', views.FavoriteListView.as_view(), name='favorites_list'),
    path("search/", views.SearchResultsView.as_view(), name="search_results"),
]
