from pydantic import BaseModel

class TokenSchema(BaseModel):
    """
    Simple token schema for sending tokens
    """
    token: str