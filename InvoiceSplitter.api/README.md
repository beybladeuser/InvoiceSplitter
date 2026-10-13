# API routes

`src/invoicesplitter_api/main.py` creates the FastAPI app and includes routers
from `src/invoicesplitter_api/routers/`. Keep route handlers grouped by domain
in separate modules, each exporting an `APIRouter`; for example, item endpoints
are in `routers/items.py`.

## Database

The PostgreSQL connection is configured through `DATABASE_HOST`, `DATABASE_PORT`,
`DATABASE_NAME`, `DATABASE_USER`, and `DATABASE_PASSWORD`. Docker Compose supplies
these settings to the API and takes the password from the root `.env` file.
For local API runs, the settings also read that root `.env` file; the database
host defaults to `localhost`.

Use `db.get_db` as a FastAPI dependency to obtain a SQLAlchemy session. ORM models
in `src/db/models.py` mirror the Flyway schema in `InvoiceSplitter.database`;
Flyway remains responsible for creating and updating database tables.