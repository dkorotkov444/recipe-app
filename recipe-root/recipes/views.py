# recipes/views.py
# Views for the recipes app

import pandas as pd
from django.shortcuts import render
from django.db import models
from django.views.generic import ListView, DetailView           # Import ListView and DetailView for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin       # For protecting Class-based views
from django.contrib.auth.decorators import login_required       # For protecting function-based views
from .models import Recipe
from .forms import RecipeSearchForm
from .utils import get_chart, get_recipe_links

# Class-based views for listing recipes and showing recipe details
class RecipesListView(LoginRequiredMixin, ListView):            # Class-based view to display a list of recipes
    model = Recipe                                              # specify the model to use for this view
    template_name = 'recipes/recipes_list.html'                 # specify the template to render
    context_object_name = 'recipes'                             # specify the context variable name to use in the template

class RecipeDetailView(LoginRequiredMixin, DetailView):         # Class-based view to display details of a single recipe
    model = Recipe                                              # specify the model to use for this view
    template_name = 'recipes/recipe_detail.html'                # specify the template to render
    context_object_name = 'recipe'                              # specify the context variable name to use in the template

# Function-based view for the Data Lab / Search
@login_required
def records(request):
    form = RecipeSearchForm(request.POST or None)       # Instantiate the form with POST data if available, otherwise create an empty form
    recipes_df = None
    chart = None
    qs = None

    if request.method == 'POST':
        recipe_name = request.POST.get('recipe_name')
        chart_type = request.POST.get('chart_type')

        # Logic for searching: Search by Name OR Ingredient Name OR Difficulty
        # Using icontains for the wildcard/partial search requirement
        if recipe_name:
            qs = Recipe.objects.filter(
                models.Q(name__icontains=recipe_name) | 
                models.Q(ingredients__name__icontains=recipe_name) |
                models.Q(difficulty__icontains=recipe_name)
            ).distinct()
        else:
            qs = Recipe.objects.all()

        if qs.exists():
            # 1. Convert QuerySet to DataFrame
            # We fetch 'id' to create links and 'ingredients' to count them
            data = []
            for obj in qs:
                item = {
                    'id': obj.id,
                    'name': obj.name,
                    'cooking_time': obj.cooking_time,
                    'difficulty': obj.difficulty,
                    'ingredient_count': obj.ingredients.count(),
                }
                data.append(item)
            
            recipes_df = pd.DataFrame(data)

            # 2. Generate Chart (Kwargs used for line chart logic)
            chart = get_chart(chart_type, recipes_df)

            # 3. Transform names into clickable HTML links
            recipes_df = get_recipe_links(recipes_df)

            # 4. Convert to HTML table (removing ID from view but keeping it for links)
            recipes_df = recipes_df.to_html(index=False, escape=False, columns=['name', 'cooking_time', 'difficulty', 'ingredient_count'])

    context = {
        'form': form,
        'recipes_df': recipes_df,
        'chart': chart,
    }

    return render(request, 'recipes/recipes_search.html', context)