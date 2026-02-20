# recipes/urls.py
from django.urls import path
from .views import home, RecipesListView, RecipeDetailView

app_name = 'recipes'

urlpatterns = [
    path('', home, name='home'),
    path('recipes/', RecipesListView.as_view(), name='recipes_list'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
]