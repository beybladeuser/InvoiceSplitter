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

### Run Keycloak (optional)

Set the Keycloak database and bootstrap admin passwords in `.env`, then start the identity services:

```powershell
docker compose --profile identity up --build -d keycloak
```

Keycloak is available at <http://localhost:8081> by default. Configure `KEYCLOAK_HOSTNAME` and `KEYCLOAK_PORT` in `.env` to use a different local address. The Keycloak database uses its own persistent volume.

### Stop the services

```powershell
docker compose down
```

This keeps the PostgreSQL data volume. To also delete the local database data, use `docker compose down -v`; this is destructive.

## Run the without Docker

This approach is only recommended for fast iteration and debugging, for proper testing and demoing pls refer to [Docker local deployment](#run-locally-with-docker-compose)

### Frontend

Install Node.js 22.12 or later, then run these commands from the repository root:

```powershell
Set-Location InvoiceSplitter.frontend
npm ci
npm run dev
```

Open the local URL printed by Vite, usually <http://localhost:5173>. This starts only the frontend development server.

### Database

There isn't any purpose on running the db locally and without docker so pls refer to [Running db in Docker](#start-the-database-and-apply-migrations)

If you still insist on running the db without docker you're on your own figuring that out