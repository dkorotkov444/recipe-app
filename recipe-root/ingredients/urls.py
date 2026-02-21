# ingredients/urls.py
from django.urls import path
from .views import IngredientsIndexView

app_name = 'ingredients'

urlpatterns = [
    path('list/', IngredientsIndexView.as_view(), name='ingredients_index'),
]