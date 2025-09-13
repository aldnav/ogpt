# Development

## Local Development Setup

### Prerequisites

- Python 3.13+
- uv package manager
- PostgreSQL (for production-like development)

### Installation

```sh
# Clone the repository
git clone git@github.com:aldnav/ogpt.git
cd ogpt

# Install dependencies
uv sync

# Set up environment files
cp .env.template .env  # Update the .env file with the correct values
cp ogpt/.pg_service.conf.template ogpt/.pg_service.conf  # Update the .pg_service.conf file with the correct values
echo "127.0.0.1:5432:DBNAME:DBUSER:DBPASSWORD" > ogpt/.pgpass  # Update the .pgpass file with the correct values

# Run migrations
just migrate

# Start development server
just runserver-dev
```

## Database

### PostgreSQL

1. Install PostgreSQL
2. Create a database
3. Create a user
4. Create a password
5. Create a service configuration

A sample setup would look like this:

```bash
psql -h 127.0.0.1 -p 5432 -d postgres -c "CREATE USER ogpt WITH PASSWORD 'ogptpass'";
psql -h 127.0.0.1 -p 5432 -d postgres -c "CREATE DATABASE ogptdb OWNER ogpt";
```

## Docker Development Setup

The project includes Docker configuration for easy development and deployment.

- Docker and Docker Compose installed
- Just command runner (optional, for convenience commands)

### Quick Start with Docker

```sh
# Clone the repository
git clone git@github.com:aldnav/ogpt.git
cd ogpt

# Start all services (Django, PostgreSQL, Nginx, Redis)
just docker-up

# Or run in background
just docker-up-detached

# Or use docker-compose directly
docker-compose up --build
```

The application will be available at:

- **Main application**: http://localhost (via Nginx)
- **Django development server**: http://localhost:8001 (direct access)
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### Docker Commands

```sh
# View all available commands
just list

# Stop all services
just docker-down

# View logs
just docker-logs

# Run Django management commands
just docker-command migrate
just docker-command createsuperuser

# Access Django shell
just docker-shell

# Run tests
just docker-test

# Clean up Docker resources
just docker-clean
```

### Docker Services

- **web**: Django application server
- **db**: PostgreSQL database
- **nginx**: Reverse proxy and static file server
- **redis**: Caching and session storage

### Environment Variables

Copy `.env.template` to `.env` and update the values as needed:

```env
# Django Configuration
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,web,nginx
DJANGO_DEBUG=False

# Port Configuration (optional - defaults shown)
DJANGO_PORT=8001
POSTGRES_PORT=5432
NGINX_HTTP_PORT=80
NGINX_HTTPS_PORT=443
REDIS_PORT=6379

# Database Configuration (for Docker)
POSTGRES_DB=ogptdb
POSTGRES_USER=ogpt
POSTGRES_PASSWORD=ogptpass
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis Configuration
REDIS_URL=redis://redis:6379/1
```

#### Port Configuration

All ports are configurable via environment variables:

- `DJANGO_PORT`: Django development server port (default: 8001)
- `POSTGRES_PORT`: PostgreSQL port (default: 5432)
- `NGINX_HTTP_PORT`: Nginx HTTP port (default: 80)
- `NGINX_HTTPS_PORT`: Nginx HTTPS port (default: 443)
- `REDIS_PORT`: Redis port (default: 6379)

If you have port conflicts, you can override them:

```bash
# Copy template and edit
cp .env.template .env
# Edit .env file to change ports, then:
docker-compose up --build

# Or override ports inline
DJANGO_PORT=8002 POSTGRES_PORT=5433 docker-compose up --build
```

### Production Considerations

For production deployment:

1. Set `DJANGO_DEBUG=False`
2. Use a strong `DJANGO_SECRET_KEY`
3. Configure proper `DJANGO_ALLOWED_HOSTS`
4. Set up SSL certificates in `docker/nginx/ssl/`
5. Use external database and Redis services
6. Configure proper logging and monitoring
