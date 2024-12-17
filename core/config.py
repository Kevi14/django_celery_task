# backend/config.py
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Django Config
DJANGO_SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG_SETTING = os.getenv("DEBUG", "False") == "True"

# Database Config
POSTGRES_DB = os.getenv("POSTGRES_DB", "test")
POSTGRES_USER = os.getenv("POSTGRES_USER", "test")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "test")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)

# Redis Config
CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://localhost:6379/0")
