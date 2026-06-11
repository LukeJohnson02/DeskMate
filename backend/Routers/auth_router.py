from fastapi import APIRouter, Depends, HTTPException, Query, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from Controllers.auth_controller import AuthController
from Controllers.user_controller import UserController
from Database.Adapters.user_adapter import UserAdapter
from Database.database import get_db
from Models.user_model import UserLogin
from Routers.user_router import get_user_controller

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_auth_controller(db: Session = Depends(get_db)) -> AuthController:
    return AuthController(UserAdapter(db))


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    controller: AuthController = Depends(get_auth_controller),
):
    try:
        return controller.authenticate_user(
            email=form_data.username, password=form_data.password
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )


@router.get("/verify-email")
def verify_email(
    token: str = Query(...), controller: UserController = Depends(get_user_controller)
):
    try:
        controller.verify_email_token(token)
        return {"message": "Email verified successfully"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")


@router.post("/password-reset-request")
def password_reset_request(
    email: str = Body(...), controller: AuthController = Depends(get_auth_controller)
):
    try:
        controller.request_password_reset(email)
        return {
            "msg": "If your email is registered, you will receive reset instructions."
        }
    except ValueError:
        # Return same message to avoid email enumeration
        return {
            "msg": "If your email is registered, you will receive reset instructions."
        }


@router.post("/password-reset")
def password_reset(
    token: str = Body(...),
    new_password: str = Body(...),
    controller: AuthController = Depends(get_auth_controller),
):
    try:
        controller.reset_password(token, new_password)
        return {"msg": "Password reset successful."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
