import jwt
import os
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from schemas import UserSchema
from utils import CRUD

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Session) \
        -> UserSchema:
    cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                   detail='Could not validate credentials')
    try:
        payload = jwt.decode(token, os.environ.get('JWT_SECRET', 'secret'), 'HS256')
        username: str = payload.get("user")
    except jwt.PyJWTError:
        raise cred_exception
    user_model = CRUD(session).get_user(username)
    if not user_model:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'User {username} doesn\'t exist')
    user: UserSchema = UserSchema(name=user_model.name, password=user_model.password)
    return user
