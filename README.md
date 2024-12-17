# Django Celery Permission-Based Questions App

This is a **Django** project that implements:
1. **Custom User Model** with extended fields.
2. **Object-Based Permissions** for CRUD operations.
3. **Django Rest Framework (DRF)** for API endpoints.
4. **Celery** for recurring background tasks, like creating random questions.
5. **Bootstrap-based Frontend** to list questions and manage filtering.


---

## Project Setup

### Step 1: Environment Variables

Create a `.env` file in the project root to configure environment variables. Example:

```dotenv
POSTGRES_DB=test
POSTGRES_USER=test
POSTGRES_PASSWORD=test
POSTGRES_HOST=db
POSTGRES_PORT=5432

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

DJANGO_SECRET_KEY=secret-key
```

---

### Step 3: Build and Run the Project with Docker Compose

Run the following command:

```bash
docker-compose up --build
```

This will:
1. Spin up the **Postgres** database.
2. Start the **Redis** server for Celery.
3. Run the Django app (`web` service) on port `8000`.
4. Start the **Celery Worker**.

---

### Step 4: Run Database Migrations and Seed Data

1. Run the database migrations:

   ```bash
   docker-compose exec web python manage.py migrate
   ```

2. Seed the database with the admin user and test users:

   ```bash
   docker-compose exec web python manage.py seed_users
   ```


3. Start the celery periodic task:

   ```bash
   docker-compose exec web python manage.py setup_periodic_tasks
   ```

---

## Usage

### Access the Application

- **Frontend**: Open your browser and navigate to `http://localhost:8000/login/`.
   - **Email**: `admin@gmail.com`
   - **Password**: `admin`

---
