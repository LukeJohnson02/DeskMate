from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from Authentication.Dependancies.auth import get_current_user
from Controllers.user_controller import UserController
from Database.Adapters.user_adapter import UserAdapter
from Database.database import get_db
from Models.user_model import UserRegister, User, UserRead

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_controller(db: Session = Depends(get_db)) -> UserController:
    adapter = UserAdapter(db)
    return UserController(adapter)


@router.get("/", response_model=list[UserRead])
def read_users(
    current_user: User = Depends(get_current_user),
    controller: UserController = Depends(get_user_controller),
):
    try:
        return controller.fetch_users(current_user)
    except PermissionError:
        raise HTTPException(status_code=403, detail="Not authorized")


@router.get("/me", response_model=UserRead)
def read_current_user(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.get("/{user_id}", response_model=UserRead)
def read_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    controller: UserController = Depends(get_user_controller),
):
    try:
        return controller.fetch_user(user_id, current_user)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Not authorized")


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    name: str = None,
    password: str = None,
    current_user: User = Depends(get_current_user),
    controller: UserController = Depends(get_user_controller),
):
    try:
        return controller.update_user(user_id, name, password, current_user)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Not authorized")


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    controller: UserController = Depends(get_user_controller),
):
    try:
        controller.delete_user(user_id, current_user)
        return {"detail": "User deleted successfully"}
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Not authorized")


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserRegister, controller: UserController = Depends(get_user_controller)
):
    try:
        return controller.register_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
