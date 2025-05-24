from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Controllers.category_controller import fetch_categories, fetch_category
from Database.database import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/")
def read_categories(db: Session = Depends(get_db)):
    return fetch_categories(db)

@router.get("/{category_id}")
def read_category(category_id: int, db: Session = Depends(get_db)):
    try:
        return fetch_category(db, category_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Category not found")
