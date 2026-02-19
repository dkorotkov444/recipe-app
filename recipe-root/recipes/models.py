# recipes/models.py
from django.db import models

# Recipes models

# Recipe difficulty choices tuple. Diffuculty is calculated automatically:
#   - easy:         cooking time < 10 minutes and number of ingredients < 4
#   - medium:       cooking time < 10 minutes and number of ingredients >= 4
#   - intermediate: cooking time >= 10 minutes and number of ingredients < 4
#   - hard:         cooking time >= 10 minutes and number of ingredients >= 4

class Recipe(models.Model):
    name = models.CharField(max_length=128, unique=True, null=False, blank=False)
    cooking_time = models.PositiveIntegerField(help_text='in minutes')
    difficulty = models.CharField(max_length=20, editable=False)
    image = models.ImageField(upload_to='recipes/', null=True, blank=True, default='no_image.png')

    # Link to the ingredients app's model using a string reference.
    # No import of the Ingredient model helps to avoid circular import issues.
    ingredients = models.ManyToManyField(
        'ingredients.Ingredient', 
        through='RecipeIngredient',
        related_name='recipes'
    )

    # Method to calculate the difficulty level based on cooking time and number of ingredients
    def calculate_difficulty(self):
        num_ingredients = self.ingredients.count()  # Count ingredients linked via the junction table
        if self.cooking_time < 10:                  # Cooking time less than 10 minutes
            self.difficulty = 'easy' if num_ingredients < 4 else 'medium'
        else:                                       # Cooking time 10 minutes or more
            self.difficulty = 'intermediate' if num_ingredients < 4 else 'hard'
        self.save(update_fields=['difficulty'])     # Save only the updated difficulty field to prevent recursion
    
    def save(self, *args, **kwargs):
        # If the recipe already exists in DB, we can update difficulty based on cooking_time
        update_fields = kwargs.get('update_fields', None)   # Grab 'update_fields' from the arguments if it exists

        # Only calculate difficulty if:
        #    - The object already exists (self.pk)
        #    - AND we aren't ALREADY just updating the difficulty (to prevent loop)
        if self.pk and (update_fields is None or 'difficulty' not in update_fields):
            self.calculate_difficulty()

        super().save(*args, **kwargs)

    # String representation
    def __str__(self):
        return f"Recipe ID: {self.id} | Name: {self.name} | Difficulty: {self.difficulty}"
    
class RecipeIngredient(models.Model):
    # Naming the fields 'recipe' and 'ingredient' lets Django handle the SQL column names correctly as recipe_id.    
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_junction')
    ingredient = models.ForeignKey('ingredients.Ingredient', on_delete=models.CASCADE, related_name='ingredient_junction')

    class Meta:
        unique_together = ('recipe', 'ingredient')  # Ensure that the same ingredient is not added multiple times to the same recipe.

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)           # Save the recipe-ingredient link first
        self.recipe.calculate_difficulty()      # Tells the linked recipe to update its difficulty

    def delete(self, *args, **kwargs):
        temp_recipe = self.recipe               # Save reference to a recipebefore deleting the link
        super().delete(*args, **kwargs)         # Delete the recipe-ingredient link
        temp_recipe.calculate_difficulty()      # Tells the linked recipe to update its difficulty after deletion

    # String representation
    def __str__(self):
        return f"Recipe: {self.recipe.name} | Ingredient: {self.ingredient.name}"