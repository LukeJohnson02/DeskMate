"""FastAPI routes for ticket categories."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Controllers.category_controller import CategoryController
from Database.Adapters.category_adapter import CategoryAdapter
from Database.database import get_db
from Models.category_model import CategoryRead

router = APIRouter(prefix="/categories", tags=["Categories"])


def get_category_controller(db: Session = Depends(get_db)) -> CategoryController:
    """Build the category controller with a request-scoped database session."""

    adapter = CategoryAdapter(db)
    return CategoryController(adapter)


@router.get("/", response_model=list[CategoryRead])
def read_categories(controller: CategoryController = Depends(get_category_controller)):
    """Return all categories that can be assigned to tickets."""

    return controller.fetch_categories()


@router.get("/{category_id}", response_model=CategoryRead)
def read_category(
    category_id: int, controller: CategoryController = Depends(get_category_controller)
):
    """Return one category by ID or raise a 404 when it does not exist."""

    category = controller.fetch_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
