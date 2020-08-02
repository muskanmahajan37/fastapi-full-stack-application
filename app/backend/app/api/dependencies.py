import jwt
from fastapi import Depends, HTTPException
from jwt import PyJWTError
from starlette import status

from app.core import security, config
from app.core.i18n import Messages
from app.crud.crud_user import get_user_by_email
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.token import TokenData


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
        db=Depends(get_db), token: str = Depends(security.oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=Messages.CANT_VALIDATE_CREDENTIALS,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, config.SECRET_KEY, algorithms=[config.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        permissions: str = payload.get("permissions")
        token_data = TokenData(email=email, permissions=permissions)
    except PyJWTError:
        raise credentials_exception
    user = get_user_by_email(db, token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: User = Depends(get_current_user),
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail=Messages.INACTIVE_USER)
    return current_user


async def get_current_active_superuser(
        current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail=Messages.USER_HAS_NO_PRIVILEGE
        )
    return current_user


def authenticate_user(db, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not security.verify_password(password, user.hashed_password):
        return False
    return user
