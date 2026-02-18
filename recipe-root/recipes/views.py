# recipes/views.py
from django.shortcuts import render

# Create your views here.
# Homepage view
def home(request):
    return render(request, 'recipes/recipes_home.html')
