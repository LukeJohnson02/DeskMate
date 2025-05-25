from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Controllers.user_controller import fetch_users, fetch_user
from Database.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def read_users(db: Session = Depends(get_db)):
    return fetch_users(db)

@router.get("/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return fetch_user(db, user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")