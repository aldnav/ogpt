# Justfile for ogpt project
# Install just: https://github.com/casey/just

# Run Django development server
runserver-dev:
    cd ogpt && uv run manage.py runserver

# Run Django development server with custom host and port
runserver-dev-ip host port="8000":
    cd ogpt && uv run manage.py runserver {{host}}:{{port}}

# Run Django shell
shell:
    cd ogpt && uv run manage.py shell

# Run Django migrations
migrate:
    cd ogpt && uv run manage.py migrate

# Create Django migrations
makemigrations:
    cd ogpt && uv run manage.py makemigrations

# Run checks
check:
    cd ogpt && uv run manage.py check

# Run Django tests
test:
    cd ogpt && uv run manage.py test

# Run pre-commit hooks
pre-commit:
    pre-commit run --all-files

# Install pre-commit hooks
install-hooks:
    pre-commit install

# Install dependencies
install:
    uv sync

# Show available commands
list:
    just --list
