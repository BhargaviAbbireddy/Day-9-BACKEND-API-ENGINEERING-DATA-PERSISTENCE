# Ticket Management API Specification

## 1. Overview
Build a REST API using FastAPI, SQLModel and SQLite.
The API manages users, tickets and comments.

## 2. Database Tables

### Users
- id: Integer, Primary Key
- name: String, Required
- email: String, Required, Unique

### Tickets
- id: Integer, Primary Key
- title: String, Required
- description: String, Optional
- status: String (open, in_progress, closed)
- priority: String (low, medium, high)
- user_id: Foreign Key referencing Users
- created_at: DateTime
- updated_at: DateTime

### Comments
- id: Integer, Primary Key
- content: String, Required
- ticket_id: Foreign Key referencing Tickets
- user_id: Foreign Key referencing Users
- created_at: DateTime

## 3. API Endpoints

### Users
- POST /users - Create a user
- GET /users - List users
- GET /users/{user_id} - Get a user

### Tickets
- POST /tickets - Create a ticket
- GET /tickets - List tickets with pagination and filters
- GET /tickets/{ticket_id} - Get a ticket
- PATCH /tickets/{ticket_id} - Partially update a ticket
- DELETE /tickets/{ticket_id} - Delete a ticket

### Comments
- POST /tickets/{ticket_id}/comments - Add a comment
- GET /tickets/{ticket_id}/comments - List ticket comments

## 4. Pagination and Filtering

GET /tickets supports:
- skip: Number of records to skip
- limit: Maximum number of records
- status: Filter by ticket status
- priority: Filter by ticket priority

Response includes:
- items
- total
- skip
- limit

## 5. Error Handling
- 400: Invalid request
- 404: Resource not found
- 422: Validation error
- 409: Duplicate user email

Errors must use a consistent JSON response format.

## 6. Testing
- Use pytest and httpx.
- Use a separate test database.
- Test successful operations and failure cases.