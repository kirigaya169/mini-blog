from fastapi import APIRouter, Depends, HTTPException, status
from schemas import TokenSchema, UserSchema
from utils import db_session_dependency, CRUD, salt
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from utils.auth import get_token
from sqlalchemy.orm import Session
from bcrypt import hashpw, checkpw

router = APIRouter(prefix='/user')


@router.post('/register', response_model=TokenSchema)
async def register(user: UserSchema, session: Session = Depends(db_session_dependency)):
    """
    Route for user registration
    :param user: user data
    :param session: session object for CRUD
    :return:
    """
    created_user: UserSchema = CRUD(session).create_user(user.name, user.password)
    return TokenSchema(access_token=get_token(created_user.name), token_type="bearer")


@router.post('/login', response_model=TokenSchema)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                session: Session = Depends(db_session_dependency)):
    """
    Route for getting JWT tokens
    :param form_data: user data
    :param session: session object for CRUD
    :return:
    """
    db_user: UserSchema | None = CRUD(session).get_user(form_data.username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'User {form_data.username} doesn\'t exist')
    if not checkpw(form_data.password.encode(), db_user.password.encode()):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Wrong password')
    return TokenSchema(access_token=get_token(form_data.username), token_type="bearer")
