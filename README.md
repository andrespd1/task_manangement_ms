# Task Management Microservice

This microservice provides endpoints for user authentication and task management, including creating, retrieving, updating, and deleting tasks.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/andrespd1/task_manangement_ms.git
   cd task-management-microservice
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running the App

### Without Docker

1. Ensure you have the necessary environment variables set up, including `DATABASE_URL` and `JWT_SECRET_KEY`.

2. Run the FastAPI development server:

   ```bash
   fastapi dev app/main.py
   ```

3. The app will be available at `http://127.0.0.1:8000`.

### With Docker

1. Build and run the Docker containers using `docker-compose`:

   ```bash
   docker compose up -d --build
   ```

2. The app will be available at `http://127.0.0.1:8000`.

## API Endpoints

### User Endpoints

- **Login**: `POST /users/login`
  - Request body: `OAuth2PasswordRequestForm`
  - Response: `Token`

- **Signup**: `POST /users/signup`
  - Request body: `UserCreate`
  - Response: `dict` containing user data and token

### Task Endpoints

- **Get All Tasks**: `GET /tasks`
  - Response: List of `Task`

- **Create Task**: `POST /tasks`
  - Request body: `TaskBase`
  - Response: `Task`

- **Update Task**: `PUT /tasks`
  - Request body: `Task`
  - Response: `Task`

- **Delete Task**: `DELETE /tasks/{task_id}`
  - Response: `dict` indicating success of deletion

## Project Structure

```
app/
├── crud/
│   ├── tasks_crud.py
│   └── users_crud.py
├── dependencies.py
├── main.py
├── models/
│   ├── task_model.py
│   └── user_model.py
├── routers/
│   ├── tasks_router.py
│   └── users_router.py
├── schemas/
│   ├── task_schema.py
│   └── user_schema.py
├── services/
│   ├── tasks_service.py
│   └── users_service.py
└── utils/
    ├── jwt_auth.py
    └── password_hashing.py
```

## Environment Variables

Ensure the following environment variables are set:

- `DATABASE_URL`: The database connection URL.
- `JWT_SECRET_KEY`: The secret key for JWT token encoding.
