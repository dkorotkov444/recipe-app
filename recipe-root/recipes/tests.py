# recipes/tests.py
from django.test import TestCase
from .models import Recipe, RecipeIngredient
from ingredients.models import Ingredient


# Create your tests here.

class RecipeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a base recipe for all tests in this class
        cls.recipe = Recipe.objects.create(name="Tea", cooking_time=5)

    def test_initial_difficulty_easy(self):
        """A new recipe with short time and 0 ingredients should be easy."""
        self.recipe.save()
        self.assertEqual(self.recipe.difficulty, 'easy')

    def test_difficulty_updates_on_time_change(self):
        """Changing cooking_time should trigger a difficulty update on save."""
        self.recipe.cooking_time = 15
        self.recipe.save()
        # 15 mins + 0 ingredients = intermediate
        self.assertEqual(self.recipe.difficulty, 'intermediate')

    def test_recipe_str_representation(self):
        """Check if the __str__ method outputs the expected format with preserved casing."""
        expected_str = f"Recipe ID: {self.recipe.id} | Name: Tea | Difficulty: easy"
        self.assertEqual(str(self.recipe), expected_str)


class RecipeIngredientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a recipe and 5 ingredient objects to use in relationship tests
        cls.recipe = Recipe.objects.create(name="Pasta", cooking_time=8)
        # These ingredients are created in the DB but not yet linked to the recipe
        cls.ingredients = [
            Ingredient.objects.create(name=f"ingredient {i}") for i in range(5)
        ]

    def test_difficulty_updates_on_adding_ingredients(self):
        """Adding ingredients via RecipeIngredient should trigger Recipe recalculation."""
        # Add 4 ingredients to the 8-minute recipe
        for i in range(4):
            RecipeIngredient.objects.create(
                recipe=self.recipe, 
                ingredient=self.ingredients[i]
            )
        
        # Refresh to see the change made by the junction table's save()
        self.recipe.refresh_from_db()
        # 8 mins + 4 ingredients = medium
        self.assertEqual(self.recipe.difficulty, 'medium')

    def test_difficulty_updates_on_removing_ingredients(self):
        """Deleting a RecipeIngredient link should trigger Recipe recalculation."""
        # Create 4 links
        links = []
        for i in range(4):
            links.append(RecipeIngredient.objects.create(
                recipe=self.recipe, 
                ingredient=self.ingredients[i]
            ))
        
        # Delete links to change count from 4 to 2
        links[0].delete()
        links[1].delete()
        
        self.recipe.refresh_from_db()
        # 8 mins + 2 ingredients = easy
        self.assertEqual(self.recipe.difficulty, 'easy')

    def test_unique_together_constraint(self):
        """Test that adding the same ingredient to a recipe twice raises an error."""
        RecipeIngredient.objects.create(recipe=self.recipe, ingredient=self.ingredients[0])
        with self.assertRaises(Exception):
            RecipeIngredient.objects.create(recipe=self.recipe, ingredient=self.ingredients[0])

    def test_cascade_delete_recipe(self):
        """Test that deleting a recipe removes its entries in the junction table."""
        RecipeIngredient.objects.create(recipe=self.recipe, ingredient=self.ingredient)
        self.recipe.delete()
        self.assertEqual(RecipeIngredient.objects.count(), 0)

    def test_recipe_ingredient_str(self):
        """Test the string representation of the junction model."""
        link = RecipeIngredient.objects.create(
            recipe=self.recipe, 
            ingredient=self.ingredients[0]
        )
        expected_str = f"Recipe: {self.recipe.name} | Ingredient: {self.ingredients[0].name}"
        self.assertEqual(str(link), expected_str)
