# ingredients/models.py
from django.db import models

# Ingredients models
class Ingredient(models.Model):
    name = models.CharField(max_length=128, unique=True, null=False, blank=False)

    def save(self, *args, **kwargs):
        self.name = self.name.strip().lower()   # Remove leading/trailing whitespace and convert to lowercase
        super().save(*args, **kwargs)           # Call the original save method

    # String representation
    def __str__(self):
        return f"Ingredient: {self.name}"