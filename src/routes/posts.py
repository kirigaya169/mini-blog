from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import SmallPostScheme, UserSchema
from typing import List, Annotated
from utils.auth import get_current_user
from utils import CRUD, db_session_dependency

router = APIRouter(prefix='/posts', dependencies=[Depends(db_session_dependency)])

UserType = Annotated[UserSchema, Depends(get_current_user)]


@router.get('/', response_model=List[SmallPostScheme])
async def get_last_posts(limit: int,
                         session: Session = Depends(db_session_dependency)):
    """
    Get last created posts
    :param limit: limitation of query result
    :param session: session object for CRUD
    :return:
    """
    return CRUD(session).get_last_posts(limit)


@router.get('/user/{user_id}', response_model=List[SmallPostScheme])
async def get_user_posts(user_id: int, limit: int,
                         user: UserType,
                         session: Annotated[Session, Depends(db_session_dependency)]):
    """
    Get posts made by user
    :param user_id: id of user to get posts from
    :param limit: limitation of answer
    :param user: JWT token of current user
    :param session: session object for CRUD
    :return:
    """
    return CRUD(session).get_user_posts(user_id, limit)
