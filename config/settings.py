import os
from pathlib import Path
import dj_database_url


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("SECRET_KEY", "your-default-secret-key")
DEBUG = os.environ.get("DEBUG", "True")
ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = 'config.urls'
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "apps.enrichment",
    "apps.common",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # or mysql, sqlite3, etc.
        'NAME': os.environ.get("DB_NAME", "your_db_name"),
        'USER': os.environ.get("DB_USER", "your_db_user"),
        'PASSWORD': os.environ.get("DB_PASSWORD", "your_password"),
        'HOST': os.environ.get("DB_HOST", "localhost"),  # or IP/hostname
        'PORT': os.environ.get("DB_PORT", "5432"),       # optional, depends on DB
        'DATABASE_URL': os.environ.get("DATABASE_URL", "postgres://user:password@localhost:5432/your_db_name"),
    }
}

CELERY_BROKER_URL = os.environ.get("REDIS_URL")

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

STATIC_URL = "/static/"