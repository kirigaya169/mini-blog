from pydantic import BaseModel


class UserSchema(BaseModel):
    """
    Base user schema with username and password
    """
    name: str
    password: str
