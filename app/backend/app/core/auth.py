from app.crud.crud_user import get_user_by_email, create_user
from app.schemas.user import UserCreate


def sign_up_new_user(db, email: str, password: str):
    user = get_user_by_email(db, email)
    if user:
        return False
    new_user = create_user(
        db,
        UserCreate(
            email=email, password=password, is_active=True, is_superuser=False,
        ),
    )
    return new_user
