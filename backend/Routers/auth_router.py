from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from Controllers.auth_controller import AuthController
from Database.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    controller = AuthController(db)
    return controller.authenticate_user(form_data.username, form_data.password)
