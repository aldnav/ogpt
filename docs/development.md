# Development

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
