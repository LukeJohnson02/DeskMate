from sqlalchemy.orm import Session
from Models import Category


class CategoryAdapter:
    def __init__(self, db: Session):
        self.db = db
        
    def get_all_categories(self):
        return self.db.query(Category).all()
    
    def get_category_by_id(self, category_id: int):
        return self.db.query(Category).filter(Category.id == category_id).first()
    
    def create_category(self, category: Category):
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
