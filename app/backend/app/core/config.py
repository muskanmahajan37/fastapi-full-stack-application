from typing import List

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

config = Config(".env")

SUPERUSER_EMAIL = config("SUPERUSER_EMAIL")
SUPERUSER_PASSWORD = config("SUPERUSER_PASSWORD")

API_V1_PREFIX = "/api"
DOCS_URL = "/api/docs"
OPENAPI_URL = "/api"
DEBUG = config("DEBUG", cast=bool, default=False)

PROJECT_NAME: str = config("PROJECT_NAME", default="FastAPI application")
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="",
)
API_PORT = 8888

VERSION: str = "0.0.1"
POSTGRES_SERVER: str = config("PG_SERVER")
POSTGRES_USER: str = config("PG_USER")
POSTGRES_PASSWORD: str = config("PG_PASSWORD")
POSTGRES_DB: str = config("PG_DB")
SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:5432/{POSTGRES_DB}"
# SQLALCHEMY_DATABASE_URI = config("DB_CONNECTION")

SECRET_KEY = config("SECRET_KEY")
ACCESS_TOKEN_EXPIRE = 60 * 24 * 8  # 8 days
ALGORITHM = "HS256"
