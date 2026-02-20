# ingredients/urls.py
from django.urls import path
from .views import home, RecipesListView, RecipeDetailView

app_name = 'ingredients'

urlpatterns = [
    path('', home, name='home'),
    path('ingredients/', IngredientsListView.as_view(), name='ingredients_list'),
]