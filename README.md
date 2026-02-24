# Recipe App (Web Application Version)

## Description
This project involves taking a Recipe app and using the Django web framework to develop a fully fledged web application with multiple users and an admin panel. It transitions the application from a command-line tool into a professional, dynamic web platform with a database backend.

## Features
* **Dynamic Data Management**: Utilizes Django's MVT (Model-View-Template) architecture to manage recipe and ingredient data.
* **Recipe List & Detail Views**: Browse all recipes or view detailed information for each recipe, including image, cooking time, difficulty, and ingredients.
* **Advanced Search & Filtering**: Search recipes by name, ingredient, or difficulty level with wildcard support.
* **Data Visualization Dashboard**: Interactive charts including bar charts (cooking time), pie charts (difficulty distribution), and line charts (complexity trends).
* **Ingredient Index**: Explore all ingredients, see how many recipes use each, and search/filter ingredients interactively.
* **Automated Difficulty Logic**: Automatically calculates and updates recipe difficulty levels based on cooking time and ingredient counts.
* **User Authentication**: Includes secure login and logout features to protect views and manage multi-user access.
* **Image Upload Support**: Upload and display images for recipes with Pillow integration.
* **Standardized Inputs**: Automatically cleans ingredient names by removing whitespace and converting to lowercase to ensure database consistency.
* **Modern UI**: Responsive, visually appealing templates for homepage, recipe list, recipe detail, and ingredient index.
* **Comprehensive Testing**: Model logic, view responses, and template integration are covered by Django TestCase tests.

## Technical Stack
* **Backend**: Python, Django.
* **Database**: SQLite (Development) / PostgreSQL (Production).
* **Frontend**: HTML, CSS.
* **Data Visualization**: Matplotlib for charts, Pandas for data processing.
* **Media Handling**: Pillow for image uploads and processing.
* **Testing**: Django TestCase for model and logic validation.

## Project Structure

```
recipe-app/
├── .gitignore           # Git ignore rules
├── README.md            # This file
├── requirements.txt     # Python dependencies
├── recipe-root/
│   ├── db.sqlite3           # SQLite database for development
│   ├── manage.py            # Django management script
│   ├── cml-prototype/       # Legacy command-line version (archived)
│   │   └── recipe_app.py
│   ├── ingredients/         # Django app: ingredients
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── migrations/
│   │   │   └── ...
│   │   └── templates/
│   │       └── ingredients/
│   │           └── ingredients_index.html
│   ├── media/               # User-uploaded media files
│   │   └── recipes/
│   ├── recipes/             # Django app: recipes
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── utils.py
│   │   ├── views.py
│   │   ├── migrations/
│   │   │   └── ...
│   │   └── templates/
│   │       └── recipes/
│   │           ├── recipes_list.html
│   │           ├── recipe_detail.html
│   │           └── recipes_search.html
│   ├── recipe-project/      # Django project config
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── wsgi.py
│   └── templates/           # Project-level templates
│       ├── base.html
│       ├── home.html
│       ├── login.html
│       └── logout_success.html
```

- The `recipes` and `ingredients` folders are Django apps with their own models, views, urls, templates, and migrations.
- The `recipe-project` folder contains the main Django project configuration.
- The `media` folder stores user-uploaded images for recipes.
- The `cml-prototype` folder contains the archived command-line version of the application.
- The database file (`db.sqlite3`) is for development; production should use PostgreSQL.

## Setup and Installation

1.  **Clone the repository**:
    ```bash
    git clone <your-repository-url>
    cd recipe-app/recipe-root
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install requirements**:
    ```bash
    pip install -r requirements.txt
    ```
    
    **Key dependencies include:**
    - **Django 6.0.2**: Web framework
    - **Pandas**: Data processing for search results
    - **Matplotlib**: Chart generation for data visualization
    - **Pillow**: Image upload and processing

4.  **Initialize the database**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create an administrative user**:
    ```bash
    python manage.py createsuperuser
    ```

## Running the Application
Start the development server with:
```bash
python manage.py runserver
```

### Available URLs:
- **Homepage**: http://127.0.0.1:8000/
- **Login**: http://127.0.0.1:8000/login/
- **Recipe List**: http://127.0.0.1:8000/recipes/list/
- **Recipe Detail**: http://127.0.0.1:8000/recipes/recipe/<id>/
- **Recipe Search & Data Visualization**: http://127.0.0.1:8000/recipes/search/
- **Ingredient Index**: http://127.0.0.1:8000/ingredients/list/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Running Tests
To verify the integrity of the models, views, and templates, run:

```bash
python manage.py test
```

---

*This project is maintained for educational and demonstration purposes.*