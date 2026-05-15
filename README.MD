# Electronics Platform

An online platform for an electronics retail network built with Django + DRF + PostgreSQL + Celery.

---
## Quick Start

```bash
# 1. Clone the repository
git clone <repo_url>
cd electronics_platform

# 2. Copy the .env file (edit if necessary)
cp .env.example .env

# 3. Run
docker compose up --build
```

After starting:
- **Admin panel**: http://localhost:8000/admin/  
  username: `head_director`, password: `admin1234`
- **API (Swagger)**: http://localhost:8000/api/schema/swagger-ui/

----
## Test Data
### `load_fixtures` (stable JSON fixtures)
This command runs automatically on `docker compose up`. It loads fixed test data from the `fixtures/` directory.

## Authentication

**Token Auth** (standard DRF):
```
POST /api-auth/login/
Authorization: Token <token>
```

**API Key**:
```
X-API-Key: <outlet_api_key>
```

## Technologies
- Python 3.12
- Django 6.0.5 + Django REST Framework 3.17.1
- PostgreSQL 16
- Celery 5.6.3 + Redis 7.4.0 + django-celery-beat
- Docker & Docker Compose


