"""Authentication dependencies shared by protected FastAPI routes."""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from Authentication.Utils.security import decode_access_token
from Database.Adapters.user_adapter import UserAdapter
from Database.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """Resolve the currently authenticated user from a bearer token.

    Args:
        token: OAuth2 bearer token extracted by FastAPI's dependency system.
        db: SQLAlchemy session dependency.

    Returns:
        The authenticated user model.

    Raises:
        HTTPException: 401 for invalid tokens or 404 when the token references
        a user that no longer exists.

    `Depends(...)` is FastAPI syntax for dependency injection: FastAPI calls
    `oauth2_scheme` and `get_db` before this function, then passes their return
    values into the parameters.
    """

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )

    user_id = int(payload.get("sub"))
    user = UserAdapter(db).get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
