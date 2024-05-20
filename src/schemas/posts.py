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
    """
    Model for request to post creation
    """
    header: str
    content: str


class UserLikeSchema(BaseModel):
    """
    Model for getting info about which user left a like or
    dislike for full post info request
    """
    id: int
    username: str


class CommentSmallSchema(BaseModel):
    """
    Model for brief information about comment
    """
    username: str
    comment: str


class PostSchema(BaseModel):
    """
    Model for full information about post
    """
    id: int
    header: str
    content: str
    likes: List[UserLikeSchema]
    dislikes: List[UserLikeSchema]
    comments: List[CommentSmallSchema]
