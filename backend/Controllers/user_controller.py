from Authentication.Utils.security import hash_password
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

    def register_user(self, user: UserRegister):
        if self.adapter.get_by_email(str(user.email)):
            raise ValueError("Email already registered")

        hashed_pw = hash_password(user.password)
        user = self.adapter.create_user(user.name, str(user.email), hashed_pw, UserRole.USER)
        return user