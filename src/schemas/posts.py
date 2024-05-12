from pydantic import BaseModel
from typing import List

class SmallPostScheme(BaseModel):
    id: int
    header: str
    content: str
    like_count: int
    dislike_count: int
    comments_count: int
