# recipes/urls.py
from django.urls import path
from .views import RecipesListView, RecipeDetailView, records

app_name = 'recipes'

urlpatterns = [
    # This becomes: http://127.0.0.1:8000/recipes/list/
    path('list/', RecipesListView.as_view(), name='recipes_list'),
    
    # This becomes: http://127.0.0.1:8000/recipes/recipe/<id>/
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),

    # Data Lab / Search view. This becomes: http://127.0.0.1:8000/recipes/search/
    path('search/', records, name='recipes_search'),
]