import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} must be set in the environment")
    return value


def _get_csv_env(name: str, default: str) -> list[str]:
    value = os.getenv(name, default)
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    secret_key: str
    algorithm: str
    access_token_expire_minutes: float
    cors_allowed_origins: list[str]
    backend_public_url: str
    frontend_public_url: str


settings = Settings(
    secret_key=get_required_env("SECRET_KEY"),
    algorithm=os.getenv("ALGORITHM", "HS256"),
    access_token_expire_minutes=float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")),
    cors_allowed_origins=_get_csv_env(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    ),
    backend_public_url=os.getenv("BACKEND_PUBLIC_URL", "http://localhost:8000").rstrip(
        "/"
    ),
    frontend_public_url=os.getenv("FRONTEND_PUBLIC_URL", "http://localhost:3000").rstrip(
        "/"
    ),
)
