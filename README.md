# InvoiceSplitter

Tool that allows you to upload images or PDFs of invoices, extract the products, and assign people to each item for splitting expenses.

## Run locally with Docker Compose

### Configure environment

From the repository root, create a local `.env` file and set a strong database password:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and replace the example `POSTGRES_PASSWORD` value. The `.env` file is ignored by Git.

### Build the images

```powershell
docker compose build
```

### Start the database and apply migrations

Start PostgreSQL and wait until its health check passes:

```powershell
docker compose up -d database
```

Apply any pending Flyway migrations:

```powershell
docker compose --profile migrations run --rm flyway
```

Flyway runs only the migrations that have not already been applied. Add future schema changes as new versioned SQL files in `InvoiceSplitter.database/migrations`.

### Run the application

```powershell
docker compose up -d
```

The frontend is available at <http://localhost:8080> by default. To use another host port, change `FRONTEND_PORT` in `.env`.

### Stop the services

```powershell
docker compose down
```

This keeps the PostgreSQL data volume. To also delete the local database data, use `docker compose down -v`; this is destructive.
