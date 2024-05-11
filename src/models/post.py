from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, TEXT, ForeignKey
from .user import UserModel
from .base import Base

from typing import List

from .like import UserPostLike
from .dislike import UserPostDislike


class PostModel(Base):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    header: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(TEXT)
    likes_count: Mapped[int] = mapped_column(Integer, default=0)
    dislikes_count: Mapped[int] = mapped_column(Integer, default=0)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete="cascade"))

    author: Mapped['UserModel'] = relationship(backref='posts')
    likes: Mapped[List['UserPostLike']] = relationship('UserPostLike')
    dislike: Mapped[List['UserPostDislike']] = relationship('UserPostDislike')

