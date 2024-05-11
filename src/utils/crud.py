from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas import UserSchema
from models import UserModel
class CRUD:
    def __init__(self, session: Session):
        self.session = session

    def get_user(self, username: str):
        stmt = select(UserModel).where(UserModel.name == username)
        user = self.session.scalars(stmt).one_or_none()
        if not user:
            return None
        return UserSchema(name=user.name, password=user.password)