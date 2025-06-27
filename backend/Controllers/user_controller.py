from datetime import timedelta, datetime

from Authentication.Utils.security import (
    hash_password,
    create_access_token,
    verify_password,
    create_email_verification_token,
    verify_email_verification_token,
)
from Authentication.Utils.email import send_verification_email
from Database.Adapters.user_adapter import UserAdapter
from Models import UserRole
from Models.user_model import UserRegister, UserLogin, User


class UserController:
    def __init__(self, adapter: UserAdapter):
        self.adapter = adapter

    def fetch_users(self, current_user: User):
        if current_user.role != UserRole.ADMIN:
            raise PermissionError("Not authorized")
        return self.adapter.get_all_users()

    def fetch_user(self, user_id: int, current_user: User):
        user = self.adapter.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        if current_user.role != UserRole.ADMIN and current_user.id != user_id:
            raise PermissionError("Not authorized")
        return user

    def register_user(self, user_data: UserRegister):
        if self.adapter.get_by_email(str(user_data.email)):
            raise ValueError("Email already registered")

        hashed_password = hash_password(user_data.password)
        new_user = self.adapter.create_user(
            str(user_data.email), user_data.name, hashed_password, UserRole.USER.value
        )

        # Generate email verification token
        verification_token = create_email_verification_token(new_user.id)

        # Send verification email (async would be better for production)
        send_verification_email(new_user.email, verification_token)

        # Return access token (optional: you may require verification before login)
        token_data = {"sub": str(new_user.id), "role": new_user.role.value}
        token = create_access_token(token_data)

        return {
            "access_token": token,
            "token_type": "bearer",
            "message": "Please verify your email",
        }

    def update_user(
        self,
        user_id: int,
        name: str = None,
        password: str = None,
        current_user: User = None,
    ):
        user = self.adapter.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        # Check permissions: admin or self
        if current_user.role != UserRole.ADMIN and current_user.id != user_id:
            raise PermissionError("Not authorized")

        if name:
            user.name = name
        if password:
            user.hashed_password = hash_password(password)

        return self.adapter.update_user(user)

    def delete_user(self, user_id: int, current_user: User):
        if current_user.role != UserRole.ADMIN:
            raise PermissionError("Only admins can delete users")

        user = self.adapter.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        self.adapter.delete_user(user)

    def verify_email_token(self, token: str):
        user_id = verify_email_verification_token(token)
        user = self.adapter.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        if user.is_verified:
            return user_id  # Already verified

        user.is_verified = True
        self.adapter.update_user(
            user
        )  # You need to add update_user method to UserAdapter
        return user_id
