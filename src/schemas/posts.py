from pydantic import BaseModel, Field
from typing import List

class SmallPostScheme(BaseModel):
    """
    Small schema for queries with big amount of posts
    """
    id: int
    header: str
    content: str
    like_count: int
    dislike_count: int
    comments_count: int


class PostRequestSchema(BaseModel):
    header: str
    content: str


class UserLikeScheme(BaseModel):
    id: int
    username: str


class CommentSmallScheme(BaseModel):
    username: str
    comment: str


class PostScheme(BaseModel):
    id: int
    header: str
    content: str
    likes: List[UserLikeScheme]
    dislikes: List[UserLikeScheme]
    comments: List[CommentSmallScheme]
