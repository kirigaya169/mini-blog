from fastapi import APIRouter, Depends, HTTPException, status
from schemas import TokenSchema, UserSchema
from utils import db_session_dependency, CRUD, salt
from utils.auth import get_token
from sqlalchemy.orm import Session
from bcrypt import hashpw, checkpw

router = APIRouter(prefix='/user')


@router.post('/register', response_model=TokenSchema)
async def reigster(user: UserSchema, session: Session = Depends(db_session_dependency)):
    created_user: UserSchema = CRUD(session).create_user(user.name, user.password)
    return TokenSchema(token=get_token(created_user.name))


@router.get('/login', response_model=TokenSchema)
async def login(username: str, password: str, session: Session = Depends(db_session_dependency)):
    db_user: UserSchema | None = CRUD(session).get_user(username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'User {username} doesn\'t exist')
    #hashed = hashpw(password.encode(), salt)
    if not checkpw(password.encode(), db_user.password.encode()):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Wrong password')
    return TokenSchema(token=get_token(username))
