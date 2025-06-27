from datetime import datetime, timedelta
from Authentication.Utils.email import send_reset_email
from Authentication.Utils.security import (
    verify_password,
    create_access_token,
    create_reset_token,
    hash_password,
)
from Database.Adapters.user_adapter import UserAdapter
from Models.user_model import UserLogin


class AuthController:
    def __init__(self, adapter: UserAdapter):
        self.user_adapter = adapter

    def authenticate_user(self, email: str, password: str):
        user = self.user_adapter.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")
        if not user.is_verified:
            raise ValueError("Email not verified")

        token_data = {"sub": str(user.id), "role": user.role}

        token = create_access_token(token_data)
        return {"access_token": token, "token_type": "bearer"}

    def request_password_reset(self, email: str):
        user = self.user_adapter.get_by_email(email)
        if not user:
            raise ValueError("Email not registered")

        token = create_reset_token(
            {"sub": str(user.id)}, expires_delta=timedelta(hours=1)
        )

        expiry = datetime.now() + timedelta(hours=1)
        self.user_adapter.set_reset_token(user, token, expiry)

        send_reset_email(user.email, token)

    def reset_password(self, token: str, new_password: str):
        user = self.user_adapter.get_user_by_reset_token(token)
        if not user:
            raise ValueError("Invalid or expired token")

        hashed = hash_password(new_password)
        self.user_adapter.update_password(user, hashed)
        self.user_adapter.clear_reset_token(user)
