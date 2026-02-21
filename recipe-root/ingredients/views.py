# ingredients/views.py
from django.views.generic import ListView      # Import ListView and DetailView for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin # For protecting Class-based views
from .models import Ingredient
from django.db.models import Count

# Class based view for listing ingredients
class IngredientsIndexView(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = 'ingredients/ingredients_index.html'
    context_object_name = 'ingredients'

    # Override the get_queryset method to annotate each ingredient with the count of recipes that use it
    def get_queryset(self):
            # We fetch ingredients and count how many recipes use them
            return Ingredient.objects.annotate(recipe_count=Count('recipes')).order_by('name')