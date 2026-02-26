# recipe/utils.py
# Utility functions for the recipes app
from io import BytesIO 
import base64
import matplotlib.pyplot as plt
import pandas as pd
from django.shortcuts import reverse

# Helper function to convert graph to base64 string
def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

# Main function to generate charts based on selection
def get_chart(chart_type, data, **kwargs):
    # Switch plot backend to Anti-Grain Geometry to avoid main thread issues
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(6,4))

    # Truncate recipe names to 18 characters followed by '...'
    truncated_names = [
        (name[:18] + '...') if len(name) > 18 else name 
        for name in data['name']
    ]

    if chart_type == '#1':
        # Bar Chart: Cooking Time Comparison
        plt.bar(truncated_names, data['cooking_time'], color='#e67e22')
        #plt.xlabel('Recipe Name')
        plt.ylabel('Cooking Time (min)')
        plt.title('Cooking Time Comparison')
        plt.xticks(rotation=45, ha='right')         # Tilt labels 45 degrees

    elif chart_type == '#2':
        # Pie Chart: Difficulty Distribution
        # count occurrences of each difficulty level
        diff_counts = data['difficulty'].value_counts()
        plt.pie(diff_counts, labels=diff_counts.index, autopct='%1.1f%%', startangle=140)
        plt.title('Difficulty Distribution')

    elif chart_type == '#3':
        # Line Chart: Ingredients vs Time
        # We need the count of ingredients which is a ManyToMany relationship
        # This assumes 'ingredient_count' was added to the dataframe in the view
        plt.plot(truncated_names, data['cooking_time'], marker='o', label='Cooking Time')
        plt.plot(truncated_names, data['ingredient_count'], marker='s', label='Ingredient Count')
        #plt.xlabel('Recipes')
        plt.title('Complexity Trends')
        plt.legend()
        plt.xticks(rotation=45, ha='right')         # Tilt labels 45 degrees
    
    plt.tight_layout()
    chart = get_graph()
    return chart

# Function to transform recipe names into clickable links
def get_recipe_links(data):
    # This iterates through the dataframe and replaces the name 
    # with an HTML anchor tag pointing to the detail view
    for index, row in data.iterrows():
        recipe_id = row['id']
        url = reverse('recipes:recipe_detail', kwargs={'pk': recipe_id})
        data.at[index, 'name'] = f'<a href="{url}" class="text-decoration-none text-primary font-weight-bold">{row["name"]}</a>'
    return data