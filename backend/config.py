"""Application configuration loaded from environment variables.

This module centralises configuration so production settings are not scattered
through controllers and routers. The `Settings` dataclass is frozen because the
values are meant to be read-only once the application starts.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def get_required_env(name: str) -> str:
    """Return a required environment variable or fail fast.

    Args:
        name: Name of the environment variable to read.

    Returns:
        The configured string value.

    Raises:
        RuntimeError: If the variable is missing or empty.

    The explicit RuntimeError is intentional: a missing secret should stop the
    backend during startup instead of silently falling back to an unsafe value.
    """

    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} must be set in the environment")
    return value


def _get_csv_env(name: str, default: str) -> list[str]:
    """Parse a comma-separated environment variable into clean string items.

    Args:
        name: Environment variable name.
        default: Comma-separated fallback used for local development.

    Returns:
        A list with whitespace removed and empty items ignored.

    A list comprehension is used here because it keeps the transformation close
    to the filtering rule: split the text, strip each item, and keep only real
    values. That makes CORS configuration resilient to spaces after commas.
    """

    value = os.getenv(name, default)
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    """Typed runtime settings used by the FastAPI application."""

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
    frontend_public_url=os.getenv(
        "FRONTEND_PUBLIC_URL", "http://localhost:3000"
    ).rstrip("/"),
)
