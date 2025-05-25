from sqlalchemy.orm import Session

from Database.Adapters.category_adapter import get_all_categories, get_category_by_id


def fetch_categories(db: Session):
    return get_all_categories(db)

def fetch_category(db: Session, category_id: int):
    category = get_category_by_id(db, category_id)
    if not category:
        raise ValueError("Category not found")
    return category
