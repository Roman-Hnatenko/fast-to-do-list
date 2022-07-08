from sqlalchemy.orm import Session

from api.db_models import UserModel
from api.exceptions import RecordNotFoundError


def get_user(db: Session, email: str) -> UserModel:
    if ddb_user := db.query(UserModel).filter(UserModel.email == email).first():
        return ddb_user
    raise RecordNotFoundError()
