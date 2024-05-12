from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import SmallPostScheme, UserSchema
from typing import List, Annotated
from utils.auth import oauth2_scheme, get_current_user
from utils import CRUD, db_session_dependency

router = APIRouter(prefix='/posts', dependencies=[Depends(db_session_dependency)])

TokenType = Annotated[str, Depends(oauth2_scheme)]

@router.get('/', response_model=List[SmallPostScheme])
async def get_last_posts(limit: int,
                         session: Session = Depends(db_session_dependency)):
    return CRUD(session).get_last_posts(limit)

@router.get('/user/{user_id}', response_model=List[SmallPostScheme])
async def get_user_posts(user_id: int, limit: int,
                         user: TokenType,
                         session: Session = Depends(db_session_dependency)):
    return CRUD(session).get_user_posts(user_id, limit)