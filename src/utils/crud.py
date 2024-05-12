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
    """
    Class for db manipulations
    """
    def __init__(self, session: Session):
        self.session = session

    def get_user(self, username: str):
        """
        Get user object by his username
        :param username:
        :return: user object or None
        """
        stmt = select(UserModel).where(UserModel.name == username)
        user = self.session.scalars(stmt).one_or_none()
        if not user:
            return None
        return UserSchema(name=user.name, password=user.password)

    def create_user(self, username: str, password: str):
        """
        Create new user with username and password
        :param username:
        :param password:
        :return: new user object
        """
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
        """
        Get amount of comments for post
        :param row:
        :return:
        """
        return self.session.scalar(select(func.count())
                                            .select_from(CommentModel)
                                            .where(CommentModel.post_id == row.id))

    def get_last_posts(self, limit: int):
        """
        Method for finding most recent posts
        :param limit: limitation of answer
        :return: array of post objects
        """
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
        """
        Get posts that were published by user
        :param user_id: id of user
        :param limit: limitation of an answer
        :return:
        """
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
