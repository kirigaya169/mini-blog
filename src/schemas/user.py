from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    name: str
    password: str
