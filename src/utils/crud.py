import os

from sqlalchemy.orm import Session
from sqlalchemy import select, func
from schemas import UserSchema, SmallPostScheme
from models import UserModel, PostModel, CommentModel


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

    def get_post_comments_count(self, row: PostModel):
        return self.session.scalar(select(func.count())
                                            .select_from(CommentModel)
                                            .where(CommentModel.post_id == row.id))

    def get_last_posts(self, limit: int):
        stmt = select(PostModel).order_by(PostModel.created_at.desc()).limit(limit)
        result = []
        for row in self.session.scalars(stmt):
            result.append(SmallPostScheme(
                id=row.id,
                header=row.header,
                content=row.content,
                like_count=row.likes_count,
                dislike_count=row.dislikes_count,
                comments_count=self.get_post_comments_count(row)
            ))
        return result

    def get_user_posts(self, user_id: int, limit: int):
        stmt = select(PostModel).where(PostModel.author_id == user_id).limit(limit)
        result = []
        for row in self.session.scalars(stmt):
            result.append(SmallPostScheme(
                id=row.id,
                header=row.header,
                content=row.content,
                like_count=row.likes_count,
                dislike_count=row.dislikes_count,
                comments_count=self.get_post_comments_count(row)
            ))
        return result
