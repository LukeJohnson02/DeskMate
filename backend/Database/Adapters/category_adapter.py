from sqlalchemy.orm import Session
from Models import Category


def get_all_categories(db: Session):
    return db.query(Category).all()

def get_category_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def create_category(db: Session, category: Category):
    db.add(category)
    db.commit()
    db.refresh(category)
    return category