# Backend (Django 5 + DRF + Channels + Celery) — Windows Setup

This guide covers both **WSL2+Docker** and **native Windows**.

---

## 0) Prerequisites
- Python **3.12+**
- Git
- One of the following:
  - **Recommended:** Docker Desktop (WSL2 backend) → run Postgres & Redis in containers.
  - **Native Windows:** Install **PostgreSQL 16** (EDB installer) and use Docker (or WSL) for Redis.

## 1) Create Virtualenv & Install Dependencies
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 2) Environment Variables
Copy the example and edit values:
```powershell
copy .env.example .env
```
**Important keys in `.env`:**
- `SECRET_KEY` — generate one: https://djecrety.ir/ (or any generator)
- `DEBUG=true`
- `ALLOWED_HOSTS=localhost,127.0.0.1`
- `DATABASE_URL=postgres://postgres:postgres@localhost:5432/odbms`
- `REDIS_URL=redis://localhost:6379/0`
- CORS: `CORS_ALLOWED_ORIGINS=http://localhost:3000`

## 3) Start a Django Project (first time only)
If you don’t already have a Django project here:
```powershell
python -m django startproject config .
```
Folder should now contain: `manage.py`, `config/` (settings/asgi/wsgi).

### 3.1) Configure `settings.py`
Create or edit `config/settings.py` like below (key parts):

```python
# config/settings.py
from pathlib import Path
import environ
import os

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY", default="changeme")
DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = [h.strip() for h in env("ALLOWED_HOSTS", default="*").split(",")]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third-party
    "rest_framework",
    "drf_spectacular",
    "django_filters",
    "corsheaders",
    "channels",
    # local apps will go here, e.g. accounts, branches, patients
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]

ASGI_APPLICATION = "config.asgi.application"
WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {"default": env.db("DATABASE_URL")}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env("REDIS_URL", default="redis://127.0.0.1:6379/1"),
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [env("REDIS_URL")]},
    }
}

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "ODBMS API",
    "VERSION": "0.1.0",
}

CORS_ALLOWED_ORIGINS = [o.strip() for o in env("CORS_ALLOWED_ORIGINS", default="http://localhost:3000").split(",")]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
```

### 3.2) `asgi.py` (Channels enabled)
```python
# config/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # "websocket": URLRouter([...])  # add later for live serial board
})
```

### 3.3) `urls.py` (health + schema)
```python
# config/urls.py
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

def healthz(_):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthz/", healthz),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]
```

## 4) Database & Redis

### Option A — Docker (recommended on Windows)
```powershell
docker run -d --name odbms-pg -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=odbms -p 5432:5432 postgres:16
docker run -d --name odbms-redis -p 6379:6379 redis:7
```
Set in `.env`:
```
DATABASE_URL=postgres://postgres:postgres@localhost:5432/odbms
REDIS_URL=redis://localhost:6379/0
```

### Option B — Native PostgreSQL 16 (EDB)
1. Install PostgreSQL 16 from EnterpriseDB.
2. Open **SQL Shell (psql)** and run:
   ```sql
   CREATE DATABASE odbms;
   CREATE USER odbms WITH ENCRYPTED PASSWORD 'odbms';
   GRANT ALL PRIVILEGES ON DATABASE odbms TO odbms;
   ```
   Then set `DATABASE_URL=postgres://odbms:odbms@localhost:5432/odbms`
3. **Redis on Windows:** run with Docker (above) or via WSL (Ubuntu: `sudo apt install redis-server`).

## 5) Migrations & Superuser
```powershell
python manage.py migrate
python manage.py createsuperuser
```

## 6) Run Servers
- **Django (HTTP/ASGI):**
  ```powershell
  daphne -b 0.0.0.0 -p 8000 config.asgi:application
  ```
  (or `python manage.py runserver` while WebSocket features are not used)
- **Celery worker & beat:**
  ```powershell
  celery -A config worker -l info
  celery -A config beat -l info
  ```

## 7) Verify
- Open http://localhost:8000/healthz/ → `{"status":"ok"}`
- API docs: http://localhost:8000/api/docs/

## 8) Next Steps
- Create your core apps (e.g., `accounts`, `branches`, `patients`)
- Wire JWT auth (DRF SimpleJWT) and role-based permissions
- Follow the milestone plan
