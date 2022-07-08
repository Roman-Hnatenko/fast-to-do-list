from api.database import async_session
from api.db_models import UserModel
from api.exceptions import RecordNotFoundError


async def get_user(email: str) -> UserModel:
    if ddb_user := await async_session.query(UserModel).filter(UserModel.email == email).first():
    # if ddb_user := await async_session.get(UserModel, {'email': email}):
        return ddb_user
    raise RecordNotFoundError()
