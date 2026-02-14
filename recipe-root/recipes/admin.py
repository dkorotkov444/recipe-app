# recipes/admin.py
from django.contrib import admin
from .models import Recipe, RecipeIngredient

# Register your models here.
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)