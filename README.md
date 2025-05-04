# Adega
Adega is a simple Inventory Management System.

## Development Environment Setup

### 1. Installing pipx
Poetry is the chosen package manager for the project.
Poetry recommends its installation through `pipx`.
Please follow the appropriate [steps](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx)
 according to your Operating System.

### 2. Install Poetry
```
pipx install poetry
```

### 3. Project installation
- On the project root `adega\`, install the project depedencies:
```
poetry install
```

- Create cache table for select2
```
poetry run python manage.py createcachetable select2_cache_table
```

- Run project's migrations:
```
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

- Create a Django `superuser` for the project. Through this user you will be able to create :
```
poetry run python manage.py createsuperuser
```

- You are all set! You can now start the Django's lightweight web server for development:
```
poetry run python manage.py runserver
```
