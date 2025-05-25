from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from Controllers.user_controller import UserController
from Database.Adapters.user_adapter import UserAdapter
from Database.database import get_db
from Models.user_model import UserRegister

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_controller(db: Session = Depends(get_db)) -> UserController:
    adapter = UserAdapter(db)
    return UserController(adapter)


@router.get("/")
def read_users(controller: UserController = Depends(get_user_controller)):
    return controller.fetch_users()


@router.get("/{user_id}")
def read_user(user_id: int, controller: UserController = Depends(get_user_controller)):
    user = controller.fetch_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
        user_data: UserRegister,
        controller: UserController = Depends(get_user_controller)
):
    try:
        user = controller.register_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
