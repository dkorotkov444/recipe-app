# Recipe App (Web Application Version)

## Description
This project involves taking a Recipe app and using the Django web framework to develop a fully fledged web application with multiple users and an admin panel. It transitions the application from a command-line tool into a professional, dynamic web platform with a database backend.

## Features
* **Dynamic Data Management**: Utilizes Django's MVT (Model-View-Template) architecture to manage recipe and ingredient data.
* **Automated Difficulty Logic**: Automatically calculates and updates recipe difficulty levels based on cooking time and ingredient counts.
* **User Authentication**: Includes secure login and logout features to protect views and manage multi-user access.
* **Data Visualization**: Implements statistical dashboards and search features for better data insights.
* **Standardized Inputs**: Automatically cleans ingredient names by removing whitespace and converting to lowercase to ensure database consistency.

## Technical Stack
* **Backend**: Python, Django.
* **Database**: SQLite (Development) / PostgreSQL (Production).
* **Frontend**: HTML, CSS.
* **Testing**: Django TestCase for model and logic validation.

## Project Structure

```
recipe-app/
├── .gitignore           (Git ignore rules)
├── README.md            (This file)
├── requirements.txt     (Python dependencies)
├── recipe-root/
│   ├── db.sqlite3           (SQLite database for development)
│   ├── manage.py            (Django management script)
│   ├── ingredients/         (Django app: ingredients)
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── views.py
│   │   └── migrations/
│   ├── recipes/             (Django app: recipes)
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── views.py
│   │   └── migrations/
│   └── recipe_project/      (Django project config)
│       ├── asgi.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
```

- The `.gitignore` file specifies files and folders to be ignored by Git version control.
- The `ingredients` and `recipes` folders are Django apps containing their own models, views, admin, and migrations.
- The `recipe_project` folder contains the main Django project configuration.
- The database file (`db.sqlite3`) is for development; production should use PostgreSQL.

## Setup and Installation

1.  **Clone the repository**:
    ```bash
    git clone <your-repository-url>
    cd recipe-root
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
    pip install django
    ```

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

Access the app at http://127.0.0.1:8000/ and the admin panel at http://127.0.0.1:8000/admin/.

## Running Tests
To verify the integrity of the models, difficulty triggers, and ingredient standardization, run:

```bash
python manage.py test
```

---

*This project is maintained for educational and demonstration purposes.*