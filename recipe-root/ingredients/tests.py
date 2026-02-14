# ingredients/tests.py
from django.test import TestCase
from django.db import IntegrityError
from .models import Ingredient

# Create your tests here.
class IngredientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # We use sugar for the static metadata tests
        Ingredient.objects.create(name="Sugar")

    def setUp(self):
        # We use salt for the creation/logic tests
        self.ingredient = Ingredient.objects.create(name="  Salt  ")

    def test_ingredient_name_metadata(self):
        """Test if the field label is correct."""
        ingredient = Ingredient.objects.get(name="sugar")   # Get an ingredient object to test
        # Get the metadata for the 'name' field and use it to query its data
        field_label = ingredient._meta.get_field('name').verbose_name     
        self.assertEqual(field_label, 'name')    # Compare the value to the expected result

    def test_ingredient_max_length(self):
           """Test that max_length is 128."""
           ingredient = Ingredient.objects.get(name="sugar")
           # Get the metadata for the 'name' field and use it to query its max_length
           max_length = ingredient._meta.get_field('name').max_length
           self.assertEqual(max_length, 128)    # Compare the value to the expected result

    def test_ingredient_creation(self):
        """Test that save() handles whitespace and lowercase."""
        # Note: setUp created "  Salt  "
        self.assertEqual(self.ingredient.name, "salt")

    def test_ingredient_uniqueness(self):
        """Test that duplicate ingredients (even with different casing) raise error."""
        with self.assertRaises(IntegrityError):
            # 'salt' already exists from setUp
            Ingredient.objects.create(name="SALT")

    def test_str_method(self):
        """Test the string representation."""
        self.assertEqual(str(self.ingredient), "Ingredient: salt")