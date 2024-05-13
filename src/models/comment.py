from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, TEXT
from .base import Base
from .user import UserModel


class CommentModel(Base):
    """
        ORM class for user_post_like model
        id - primary key of row
        user_id - id of user who left this like
        post_id - id of post
        """
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    comment = mapped_column(TEXT, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))

    author: Mapped['UserModel'] = relationship()