from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from Controllers.auth_controller import AuthController
from Database.Adapters.user_adapter import UserAdapter
from Database.database import get_db
from Models.user_model import UserLogin

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_auth_controller(db: Session = Depends(get_db)) -> AuthController:
    return AuthController(UserAdapter(db))

@router.post("/login")
def login(credentials: UserLogin, controller: AuthController = Depends(get_auth_controller)):
    try:
        return controller.authenticate_user(credentials)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")