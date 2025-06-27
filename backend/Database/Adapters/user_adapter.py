from datetime import datetime

from sqlalchemy.orm import Session
from Models import User


class UserAdapter:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_all_users(self):
        return self.db.query(User).all()

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, email: str, name: str, hashed_password: str, role: str):
        new_user = User(
            email=email, name=name, hashed_password=hashed_password, role=role
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def update_user(self, user: User):
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user: User):
        self.db.delete(user)
        self.db.commit()

    def set_reset_token(self, user: User, token: str, expiry: datetime):
        user.reset_token = token
        user.reset_token_expiry = expiry
        self.db.commit()
        self.db.refresh(user)

    def get_user_by_reset_token(self, token: str):
        now = datetime.now()
        return (
            self.db.query(User)
            .filter(User.reset_token == token, User.reset_token_expiry > now)
            .first()
        )

    def clear_reset_token(self, user: User):
        user.reset_token = None
        user.reset_token_expiry = None
        self.db.commit()
        self.db.refresh(user)

    def update_password(self, user: User, hashed_password: str):
        user.hashed_password = hashed_password
        self.db.commit()
        self.db.refresh(user)
