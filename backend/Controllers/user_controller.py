from Database.Adapters.user_adapter import UserAdapter


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