from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from .base import Base


class UserModel(Base):
    """
        ORM class for user model
        id - id of row
        name - name of user
        password - hashed password
    """
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
