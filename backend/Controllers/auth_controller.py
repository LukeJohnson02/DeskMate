from datetime import timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status
from Authentication.Utils.security import verify_password, create_access_token
from Database.Adapters.user_adapter import UserAdapter


class AuthController:
    def __init__(self, db: Session):
        self.user_adapter = UserAdapter(db)

    def authenticate_user(self, email: str, password: str):
        user = self.user_adapter.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        token = create_access_token(
            data={"sub": str(user.id), "role": user.role.name},
            expires_delta=timedelta(minutes=60)
        )
        return {"access_token": token, "token_type": "bearer"}
