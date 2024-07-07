from datetime import timedelta
from typing import Annotated
from app.utils.jwt_auth import Token
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
import app.services.users_service as users_service
from app.schemas.user_schema import UserCreate
from app.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(get_db)])


@router.get("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = router.dependencies[0],
) -> Token:
    try:
        return users_service.login_user(db, form_data.username, form_data.password)
    except HTTPException as e:
        raise HTTPException(e.status_code, e.detail)


@router.post("/signup")
async def sign_up(user: UserCreate, db: Session = router.dependencies[0]):
    return users_service.register_user(db, user)
