from sqlalchemy.orm import Session

from api.ddb_models import UserModel
from api.settings import pwd_context

from .models import UserInput


def create_user(db: Session, user: UserInput) -> UserModel:
    db_user = UserModel(
        email=user.email,
        name=user.name,
        hashed_password=pwd_context.hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
