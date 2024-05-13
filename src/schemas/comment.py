from pydantic import BaseModel

class CommentSchema(BaseModel):
    comment: str