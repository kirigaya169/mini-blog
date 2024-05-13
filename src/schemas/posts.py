from pydantic import BaseModel, Field
from typing import List

class SmallPostSchema(BaseModel):
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


class UserLikeSchema(BaseModel):
    id: int
    username: str


class CommentSmallSchema(BaseModel):
    username: str
    comment: str


class PostSchema(BaseModel):
    id: int
    header: str
    content: str
    likes: List[UserLikeSchema]
    dislikes: List[UserLikeSchema]
    comments: List[CommentSmallSchema]
