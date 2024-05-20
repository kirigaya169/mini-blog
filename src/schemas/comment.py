from pydantic import BaseModel


class CommentSchema(BaseModel):
    """
    Model for comment input
    """
    comment: str
