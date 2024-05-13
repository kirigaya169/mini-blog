from pydantic import BaseModel

class TokenSchema(BaseModel):
    """
    Simple token schema for sending tokens
    """
    access_token: str
    token_type: str