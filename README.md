# InvoiceSplitter

Tool that allows you to upload images or PDFs of invoices, extract the products, and assign people to each item for splitting expenses.

## Run locally with Docker Compose

### Configure environment

From the repository root, create a local `.env` file and set a strong database password:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and replace all example password values with strong passwords. The `.env` file is ignored by Git.

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

The frontend is available at <http://localhost:8080>, the API at <http://localhost:8000>, and Keycloak at <http://localhost:8081> by default. To use different host ports, change `FRONTEND_PORT`, `API_PORT`, or `KEYCLOAK_PORT` in `.env`.

Keycloak starts with the rest of the Compose services and uses its own persistent database volume. Configure `KEYCLOAK_HOSTNAME` in `.env` if you change its local address.

### Stop the services

```powershell
docker compose down
```

This keeps the PostgreSQL data volume. To also delete the local database data, use `docker compose down -v`; this is destructive.

## Run the app code without Docker

This runs the React frontend and FastAPI API directly on your machine. PostgreSQL and Keycloak still run in Docker Compose; running those services natively is not covered here.

### Start PostgreSQL and Keycloak

If you have not created `.env` yet, copy the example and replace its placeholder passwords with strong values:

```powershell
Copy-Item .env.example .env
```

Start the supporting services and apply database migrations:

```powershell
docker compose up -d database keycloak-database keycloak
docker compose --profile migrations run --rm flyway
```

### Run the API

Install Python 3.14 and `uv`. In a new terminal from the repository root, run:

```powershell
Set-Location InvoiceSplitter.api
uv sync --locked
uv run fastapi dev src/main.py --host 0.0.0.0 --port 8000
```

The API is available at <http://localhost:8000>; its interactive docs are at <http://localhost:8000/docs>.

### Run the frontend

Install Node.js 22.12 or later. In another terminal from the repository root, run:

```powershell
Set-Location InvoiceSplitter.frontend
npm ci
npm run dev
```

Open the local URL printed by Vite, usually <http://localhost:5173>. This starts only the frontend development server.

### Database

There isn't any purpose on running the db locally and without docker so pls refer to [Running db in Docker](#start-the-database-and-apply-migrations)

If you still insist on running the db without docker you're on your own figuring that out