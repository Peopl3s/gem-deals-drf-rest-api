import os

from dotenv import find_dotenv, load_dotenv

from .base import *

env_file = find_dotenv("env.local")
load_dotenv(env_file)


DJANGO_SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")


DEBUG = int(os.getenv("DEBUG", default=1))

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(" ")

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DATABASE_ENGINE"),
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CACHES = {
    "default": {
        "BACKEND": os.getenv("CACHE_BACKEND"),
        "LOCATION": os.getenv("CACHE_LOCATION"),
    }
}
