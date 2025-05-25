from Authentication.Utils.security import verify_password, create_access_token
from Database.Adapters.user_adapter import UserAdapter
from Models.user_model import UserLogin


class AuthController:
    def __init__(self, adapter: UserAdapter):
        self.user_adapter = adapter

    def authenticate_user(self, credentials: UserLogin):
        user = self.user_adapter.get_by_email(str(credentials.email))
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise ValueError("Invalid email or password")

        token_data = {
            "sub": str(user.id),
            "role": user.role
        }
        token = create_access_token(token_data)
        return {"access_token": token, "token_type": "bearer"}
