# ingredients/tests.py
from django.test import TestCase
from django.db import IntegrityError
from .models import Ingredient
from django.urls import reverse
from django.contrib.auth.models import User # Added for auth

# --- Models tests ---
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

# --- Views tests ---
class IngredientViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testchef', password='password123')    # Create a test user
        cls.ingredient1 = Ingredient.objects.create(name="apple")
        cls.ingredient2 = Ingredient.objects.create(name="banana")

    def setUp(self):
        self.client.login(username='testchef', password='password123')  # Log in the user before each test

    def test_ingredient_index_view_status_and_template(self):
        url = reverse('ingredients:ingredients_index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)     # Now returns 200 because we are logged in
        self.assertTemplateUsed(response, 'ingredients/ingredients_index.html')
        self.assertContains(response, self.ingredient1.name)
        self.assertContains(response, self.ingredient2.name)

    def test_ingredient_index_recipe_count(self):
        url = reverse('ingredients:ingredients_index')
        response = self.client.get(url)
        # Should show recipe_count for each ingredient (should be 0 here)
        self.assertContains(response, '0')

# --- Functional tests for ingredient_index template ---
class IngredientIndexFunctionalTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='sous_chef', password='password123')
        # Create ingredients with different first letters for regrouping test
        cls.ing1 = Ingredient.objects.create(name="Apple")
        cls.ing2 = Ingredient.objects.create(name="Banana")

    def setUp(self):
        self.client.login(username='sous_chef', password='password123')

    def test_ingredient_regrouping_logic(self):
        """Verify ingredients are grouped by the first letter in the template."""
        url = reverse('ingredients:ingredients_index')
        response = self.client.get(url)
        # Check for regroup headers
        self.assertContains(response, 'A')
        self.assertContains(response, 'B')

    def test_data_attributes_for_js_filter(self):
        """Verify the HTML contains data-name attributes required for JS filtering."""
        url = reverse('ingredients:ingredients_index')
        response = self.client.get(url)
        # Verify data-name attribute exists for the JS logic to grab
        self.assertContains(response, 'data-name="apple"')