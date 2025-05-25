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
        new_user = User(email=email, name=name, hashed_password=hashed_password, role=role)
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