"""Password hashing and JWT token helpers for authentication workflows."""

from datetime import datetime, timedelta
from typing import Any

from jose import jwt, JWTError
from passlib.context import CryptContext

from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create a signed JWT access token.

    Args:
        data: Claims to encode in the token, normally including `sub`.
        expires_delta: Optional custom lifetime for special cases.

    Returns:
        A compact JWT string signed with the configured secret key.

    The function copies `data` before adding `exp` so callers do not see their
    input dictionary mutated. The expression using `or` selects a custom expiry
    when provided, otherwise it uses the normal configured access-token timeout.
    """

    to_encode = data.copy()
    expire = datetime.now() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def hash_password(password: str) -> str:
    """Hash a plain-text password with Passlib's bcrypt context."""

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compare a user-entered password against a stored password hash."""

    return pwd_context.verify(plain_password, hashed_password)


def decode_access_token(token: str) -> dict[str, Any] | None:
    """Decode and validate an access token.

    Args:
        token: Encoded JWT from the Authorization header.

    Returns:
        The decoded payload when valid, otherwise `None`.

    Returning `None` keeps the lower-level JWT error details away from route
    handlers. The dependency layer converts this into a consistent HTTP 401.
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def create_email_verification_token(
    user_id: int, expires_delta: timedelta = timedelta(hours=24)
) -> str:
    """Create a JWT used to verify a user's email address.

    Args:
        user_id: Database ID of the user being verified.
        expires_delta: Lifetime of the verification link.

    Returns:
        Signed JWT containing the user ID and expiry.
    """

    expire = datetime.now() + expires_delta
    to_encode = {"user_id": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_email_verification_token(token: str) -> int:
    """Validate an email verification token and return its user ID.

    Args:
        token: Encoded verification JWT.

    Returns:
        User ID embedded in the token.

    Raises:
        ValueError: If the token is expired, malformed, or missing a user ID.
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise ValueError("Invalid token")
        return user_id
    except JWTError:
        raise ValueError("Invalid token")


def create_reset_token(data: dict, expires_delta: timedelta) -> str:
    """Create a signed JWT for password reset flows.

    Args:
        data: Claims to include, usually the user's subject ID.
        expires_delta: How long the reset token should remain usable.

    Returns:
        Signed JWT reset token.
    """

    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
