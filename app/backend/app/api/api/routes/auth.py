from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_db, authenticate_user
from app.core import config
from app.core import security
from app.core.auth import sign_up_new_user
from app.core.i18n import Messages
from app.models.user import User

router = APIRouter()


@router.post("/token")
async def login(
        db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user: User = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=Messages.INCORRECT_CREDENTIALS,
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE)
    if user.is_superuser:
        permissions = "admin"
    else:
        permissions = "user"
    access_token = security.create_access_token(
        data={"sub": user.email, "permissions": permissions},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup")
async def signup(
        db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = sign_up_new_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Messages.ACCOUNT_EXISTS,
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRE
    )
    if user.is_superuser:
        permissions = "admin"
    else:
        permissions = "user"
    access_token = security.create_access_token(
        data={"sub": user.email, "permissions": permissions},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
