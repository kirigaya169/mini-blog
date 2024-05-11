import os

from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas import UserSchema
from models import UserModel


from fastapi import HTTPException, status
from bcrypt import hashpw, gensalt
from dotenv import load_dotenv
load_dotenv()
salt = gensalt()
class CRUD:
    def __init__(self, session: Session):
        self.session = session

    def get_user(self, username: str):
        stmt = select(UserModel).where(UserModel.name == username)
        user = self.session.scalars(stmt).one_or_none()
        if not user:
            return None
        return UserSchema(name=user.name, password=user.password)

    def create_user(self, username: str, password: str):
        stmt = select(UserModel).where(UserModel.name == username)
        if self.session.scalars(stmt).one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'User {username} already exists')
        hashed = hashpw(password.encode(), salt).decode()
        user = UserModel(name=username, password=hashed)
        self.session.add(user)
        self.session.commit()
        return UserSchema(name=username, password=hashed)