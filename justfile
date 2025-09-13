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

# Docker commands
docker-up:
    docker-compose up --build

docker-up-detached:
    docker-compose up --build -d

docker-down:
    docker-compose down

docker-down-volumes:
    docker-compose down -v

docker-logs:
    docker-compose logs -f

docker-logs-service service:
    docker-compose logs -f {{service}}

docker-shell:
    docker-compose exec web python ogpt/manage.py shell --settings=ogpt.docker_settings

docker-test:
    docker-compose exec web python ogpt/manage.py test --settings=ogpt.docker_settings

docker-createsuperuser:
    docker-compose exec web python ogpt/manage.py createsuperuser --settings=ogpt.docker_settings

docker-collectstatic:
    docker-compose exec web python ogpt/manage.py collectstatic --noinput --settings=ogpt.docker_settings

docker-migrate:
    docker-compose exec web python ogpt/manage.py migrate --settings=ogpt.docker_settings

docker-command command:
    docker-compose exec web python ogpt/manage.py {{command}} --settings=ogpt.docker_settings

docker-ps:
    docker-compose ps

docker-rebuild service:
    docker-compose up --build {{service}}

docker-clean:
    docker system prune -f
    docker volume prune -f

# Show available commands
list:
    just --list
