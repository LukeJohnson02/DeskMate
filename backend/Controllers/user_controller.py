from sqlalchemy.orm import Session
from Database.Adapters.user_adapter import get_all_users, get_user_by_id

def fetch_users(db: Session):
    return get_all_users(db)

def fetch_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")
    return user