from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Controllers.user_controller import UserController
from Database.Adapters.user_adapter import UserAdapter
from Database.database import get_db

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