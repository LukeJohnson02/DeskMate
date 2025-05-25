from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Controllers.category_controller import CategoryController
from Database.Adapters.category_adapter import CategoryAdapter
from Database.database import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])

def get_category_controller(db: Session = Depends(get_db)) -> CategoryController:
    adapter = CategoryAdapter(db)
    return CategoryController(adapter)

@router.get("/")
def read_categories(controller: CategoryController = Depends(get_category_controller)):
    return controller.fetch_categories()

@router.get("/{category_id}")
def read_category(category_id: int, controller: CategoryController = Depends(get_category_controller)):
    category = controller.fetch_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category