# API routes

`src/invoicesplitter_api/main.py` creates the FastAPI app and includes routers
from `src/invoicesplitter_api/routers/`. Keep route handlers grouped by domain
in separate modules, each exporting an `APIRouter`; for example, item endpoints
are in `routers/items.py`.

## Database

The PostgreSQL connection requires `DATABASE_HOST`, `DATABASE_PORT`,
`DATABASE_NAME`, `DATABASE_USER`, and `DATABASE_PASSWORD`. Docker Compose uses
these root `.env` values for the database and migration service, then supplies
the API with its internal database hostname and port. For local API runs, set the
same values in the root `.env` file; see `.env.example` for local connection
values.

Use `db.get_db` as a FastAPI dependency to obtain a SQLAlchemy session. ORM models
in `src/db/models.py` mirror the Flyway schema in `InvoiceSplitter.database`;
Flyway remains responsible for creating and updating database tables.