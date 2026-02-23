from django import forms

# Choices for the chart type dropdown
CHART__CHOICES = (
    ('#1', 'Bar Chart (Cooking Time)'),
    ('#2', 'Pie Chart (Difficulty Distribution)'),
    ('#3', 'Line Chart (Ingredients vs Time)'),
)

# Class-based form for searching recipes and selecting chart type
class RecipeSearchForm(forms.Form):
    # Search field for recipe name or ingredients
    recipe_name = forms.CharField(
        max_length=128, 
        required=False, 
        label="Search Recipes",
        # Adding a placeholder to explain empty field behavior
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter name or ingredient (leave blank for all)'
        })
    )
    
    # Dropdown for selecting the visualization type, 'initial' ensures a chart is selected by default
    chart_type = forms.ChoiceField(
        choices=CHART__CHOICES, 
        required=False,
        label="Chart Type",
        initial='#1' 
    )