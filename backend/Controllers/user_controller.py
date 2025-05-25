from Authentication.Utils.security import hash_password, create_access_token
from Database.Adapters.user_adapter import UserAdapter
from Models import UserRole
from Models.user_model import UserRegister


class UserController:
    def __init__(self, adapter: UserAdapter):
        self.adapter = adapter

    def fetch_users(self):
        return self.adapter.get_all_users()

    def fetch_user(self, user_id: int):
        user = self.adapter.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user

    def register_user(self, user_data: UserRegister):
        if self.adapter.get_by_email(str(user_data.email)):
            raise ValueError("Email already registered")

        hashed_password = hash_password(user_data.password)
        new_user = self.adapter.create_user(str(user_data.email), user_data.name, hashed_password, UserRole.USER)

        # Generate token
        token_data = {
            "sub": str(new_user.id),
            "role": new_user.role
        }
        token = create_access_token(token_data)

        return {"access_token": token, "token_type": "bearer"}