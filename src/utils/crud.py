import datetime

from bcrypt import hashpw, gensalt
from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models import (
    UserModel,
    PostModel,
    CommentModel,
    UserPostLikeModel,
    UserPostDislikeModel
)
from schemas import (
    UserSchema,
    SmallPostSchema,
    PostRequestSchema,
    UserLikeSchema,
    PostSchema,
    CommentSmallSchema
)

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
            result.append(SmallPostSchema(
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
            result.append(SmallPostSchema(
                id=row.id,
                header=row.header,
                content=row.content,
                like_count=row.likes_count,
                dislike_count=row.dislikes_count,
                comments_count=self.get_post_comments_count(row)
            ))
        return result

    def create_post(self, username: str, post: PostRequestSchema):
        stmt = select(UserModel).where(UserModel.name == username)
        post_model = PostModel(header=post.header, content=post.content,
                               author_id=self.session.scalars(stmt).one().id,
                               created_at=datetime.datetime.now())
        self.session.add(post_model)
        self.session.commit()
        self.session.refresh(post_model)
        return SmallPostSchema(id=post_model.id,
                               header=post_model.header,
                               content=post_model.content,
                               like_count=0,
                               dislike_count=0,
                               comments_count=0)

    def add_like(self, username: str, post_id: int, is_like: bool):
        if is_like:
            model_class = UserPostLikeModel
        else:
            model_class = UserPostDislikeModel
        user_id = (self.session.scalars(select(UserModel).
                                        where(UserModel.name == username)).
                   one().id)
        post_object = self.session.scalars(select(PostModel).where(PostModel.id == post_id)).one_or_none()

        if post_object is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Post with this ID doesn\'t exist')
        if (self.session.scalars(select(model_class)
                                         .where(model_class.post_id == post_object.id)
                                         .where(model_class.user_id == user_id))).one_or_none() is not None:

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='User cannot add like/dislike to this post')
        if is_like:
            post_object.likes_count += 1
        else:
            post_object.dislikes_count += 1
        like_object = model_class(user_id=user_id, post_id=post_id)
        self.session.add_all([like_object, post_object])
        self.session.commit()

    def add_comment(self, username: str, post_id: int, comment: str):
        user_id = self.session.scalars(select(UserModel).where(UserModel.name == username)).one().id
        if self.session.scalars(select(PostModel).where(PostModel.id == post_id)).one_or_none() is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='there is no post with this id')
        comment_object = CommentModel(comment=comment, post_id=post_id, user_id=user_id)
        self.session.add(comment_object)
        self.session.commit()

    def get_post_info(self, post_id: int):
        post = self.session.scalars(select(PostModel).where(PostModel.id == post_id)).one_or_none()
        if post is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='There is no post with this ID')
        comments = []
        for comment in self.session.execute(select(CommentModel, UserModel)
                                                    .join(UserModel)
                                                    .filter(UserModel.id == CommentModel.user_id)
                                                    .where(CommentModel.post_id == post_id)):
            comments.append(CommentSmallSchema(
                username=comment.UserModel.name,
                comment=comment.CommentModel.comment
            ))
        likes = []
        for like in self.session.execute(select(UserPostLikeModel, UserModel)
                                                 .join(UserModel)
                                                 .filter(UserModel.id == UserPostLikeModel.user_id)
                                                 .where(UserPostLikeModel.post_id == post_id)):
            likes.append(UserLikeSchema(
                id=like.UserModel.id,
                username=like.UserModel.name
            ))

        dislikes = []
        for dislike in self.session.execute(select(UserPostDislikeModel, UserModel)
                                                    .join(UserModel)
                                                    .filter(UserModel.id == UserPostDislikeModel.user_id)
                                                    .where(UserPostDislikeModel.post_id == post_id)):
            dislikes.append(UserLikeSchema(
                id=dislike.UserModel.id,
                username=dislike.UserModel.name
            ))
        return PostSchema(
            id=post_id,
            header=post.header,
            content=post.content,
            likes=likes,
            dislikes=dislikes,
            comments=comments
        )
