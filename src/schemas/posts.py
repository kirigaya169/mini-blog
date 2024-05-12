from pydantic import BaseModel
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
