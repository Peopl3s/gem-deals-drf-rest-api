from dotenv import find_dotenv, load_dotenv

from .base import *

env_file = find_dotenv("env.prod")
load_dotenv(env_file)

DJANGO_SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DEBUG = int(os.getenv("DEBUG"))

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(" ")


DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DATABASE_ENGINE"),
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("DATABASE_HOST"),
        "PORT": os.environ.get("DATABASE_PORT"),
    }
}

CACHES = {
    "default": {
        "BACKEND": os.getenv("CACHE_BACKEND"),
        "LOCATION": os.getenv("CACHE_LOCATION"),
    }
}
