# Dockerfile for Django project Adega
# python 3.13 and Django 5.2
# Dependencies should be installed via poetry 2.1.3
FROM python:3.13

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=2.1.3
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry/venv
ENV PATH="${POETRY_VENV}/bin:$PATH"

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Clone the repository
# RUN git clone https://github.com/rocharv/adega.git /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install project dependencies (but do not include dev dependencies)
RUN poetry install --no-interaction --no-ansi

# Expose the port the app runs on
EXPOSE 8000

 # Start the application
CMD poetry run python manage.py createcachetable select2_cache_table && \
    poetry run python manage.py collectstatic --noinput && \
    poetry run python manage.py makemigrations && \
    poetry run python manage.py migrate --run-syncdb && \
    poetry run python manage.py createsuperuser --noinput && \
    poetry run gunicorn --bind 0.0.0.0:8000 adega.wsgi:application