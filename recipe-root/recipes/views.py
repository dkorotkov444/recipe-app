# recipes/views.py
from django.shortcuts import render
from django.views.generic import ListView, DetailView      # Import ListView and DetailView for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin # For protecting Class-based views
from .models import Recipe

# Homepage view
def home(request):
    return render(request, 'recipes/recipes_home.html')

# Class-based views for listing recipes and showing recipe details
class RecipesListView(LoginRequiredMixin, ListView):          # class-based view to display a list of recipes
    model = Recipe                        # specify the model to use for this view
    template_name = 'recipes/recipes_list.html'   # specify the template to render
    context_object_name = 'recipes'       # specify the context variable name to use in the template

class RecipeDetailView(LoginRequiredMixin, DetailView):      # class-based view to display details of a single recipe
    model = Recipe                        # specify the model to use for this view
    template_name = 'recipes/recipe_detail.html' # specify the template to render
    context_object_name = 'recipe'        # specify the context variable name to use in the template
