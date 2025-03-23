# Full-Stack Django React Application with Docker and Docker Compose

A full-stack web application built with Django REST Framework and React.

## Project Overview

- User authentication and authorization
- Auth0 for social login
- Tailwind CSS for styling
- Profile management with customizable user details
- Email verification system
- Background task processing with Celery
- Redis caching and message broker
- PostgreSQL database
- Docker containerization

## Tech Stack

### Backend
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- JWT Authentication

### Infrastructure  
- Docker
- Docker Compose

## Prerequisites

- Docker
- Docker Compose

## Environment Setup

1. Clone the repository
2. Copy the environment file:
```bash
cd backend
cp .env.example .env
```

3. Update the environment variables in the `.env` file:
```markdown
SECRET_KEY=changeme
DEBUG=True
POSTGRES_DB=changeme
POSTGRES_USER=changeme
POSTGRES_PASSWORD=changeme
DB_HOST=postgres
```

4. Build and start the Docker containers:
```bash
docker-compose up --build
```

This will start:

* Django backend server (:8000)
* React frontend (:3000)
* PostgreSQL database (:5433)
* Redis (:6379)
* Celery worker
* Celery beat scheduler
