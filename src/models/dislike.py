from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey
from .base import Base


class UserPostDislike(Base):
    """
    ORM class for user_post_dislike model
    id - primary key of row
    user_id - id of user who left this dislike
    post_id - id of post
    """
    __tablename__ = 'user_post_dislike'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))