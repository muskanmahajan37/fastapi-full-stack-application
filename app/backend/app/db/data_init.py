#!/usr/bin/env python3

from app.core import config
from app.crud.crud_user import create_user, get_user_by_email
from app.db.session import SessionLocal
from app.schemas.user import UserCreate


def init() -> None:
    db = SessionLocal()
    user = get_user_by_email(db,email=config.SUPERUSER_EMAIL)
    if not user:
        create_user(
            db,
            UserCreate(
                email=config.SUPERUSER_EMAIL,
                password=config.SUPERUSER_PASSWORD,
                is_active=True,
                is_superuser=True,
            ),
        )



if __name__ == "__main__":
    print(f"Creating superuser {config.SUPERUSER_EMAIL}")
    init()
    print("Superuser created")
