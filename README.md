\# Ticket Management API



A REST API built using FastAPI, SQLModel, SQLite and Alembic to manage users, tickets and comments.



\## Features

\- User creation and retrieval

\- Ticket CRUD operations

\- Comment creation and retrieval

\- Pagination and filtering by status and priority

\- Input validation and error handling

\- Database migrations using Alembic

\- Integration tests using pytest and httpx

\- Synthetic seed data



\## Installation



Install dependencies:



```bash

uv sync

```



\## Database Setup



```bash

uv run alembic upgrade head

```



\## Run the API



```bash

uv run uvicorn ticket\_api.main:app --reload

```



API URL: http://127.0.0.1:8000



Swagger documentation: http://127.0.0.1:8000/docs



\## API Endpoints



\### Users

\- POST /users

\- GET /users

\- GET /users/{user\_id}



\### Tickets

\- POST /tickets

\- GET /tickets

\- GET /tickets/{ticket\_id}

\- PATCH /tickets/{ticket\_id}

\- DELETE /tickets/{ticket\_id}



\### Comments

\- POST /tickets/{ticket\_id}/comments

\- GET /tickets/{ticket\_id}/comments



\## Pagination and Filtering



Example:



```text

/tickets?skip=0\&limit=10\&status=open\&priority=high

```



\## Seed Data



```bash

uv run python -m ticket\_api.seed

```



\## Run Integration Tests



```bash

uv run pytest -v

```



Tests use a separate temporary SQLite database.



\## Database Migrations



Create migration:



```bash

uv run alembic revision --autogenerate -m "migration message"

```



Apply migration:



```bash

uv run alembic upgrade head

```



Check migration:



```bash

uv run alembic current

```



\## Technology Stack

\- Python

\- FastAPI

\- SQLModel

\- SQLite

\- Alembic

\- Pytest

\- HTTPX

\- Uvicorn

