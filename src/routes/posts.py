from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import (
    SmallPostSchema,
    UserSchema,
    PostRequestSchema,
    CommentSchema,
    PostSchema
)
from typing import List, Annotated
from utils.auth import get_current_user
from utils import CRUD, db_session_dependency

router = APIRouter(prefix='/posts', dependencies=[Depends(db_session_dependency)])

UserType = Annotated[UserSchema, Depends(get_current_user)]
SessionDep = Annotated[Session, Depends(db_session_dependency)]


@router.get('/', response_model=List[SmallPostSchema])
async def get_last_posts(limit: int,
                         session: SessionDep):
    """
    Get last created posts
    :param limit: limitation of query result
    :param session: session object for CRUD
    :return:
    """
    return CRUD(session).get_last_posts(limit)


@router.get('/user/{user_id}', response_model=List[SmallPostSchema])
async def get_user_posts(user_id: int, limit: int,
                         user: UserType,
                         session: SessionDep):
    """
    Get posts made by user
    :param user_id: id of user to get posts from
    :param limit: limitation of answer
    :param user: current user
    :param session: session object for CRUD
    :return:
    """
    return CRUD(session).get_user_posts(user_id, limit)


@router.post('/', response_model=SmallPostSchema)
async def create_post(post: PostRequestSchema, user: UserType,
                      session: SessionDep):
    """
    Route for post creation
    :param post: post information
    :param user: current user
    :param session:
    :return:
    """
    return CRUD(session).create_post(user.name, post)


@router.post('/add_like/{post_id}')
async def add_like(post_id: int, user: UserType, session: SessionDep):
    """
    Add like to post
    :param post_id: id of a post
    :param user: current user
    :param session:
    :return:
    """
    CRUD(session).add_like(user.name, post_id, True)
    return {'status': 'ok'}


@router.post('/add_dislike/{post_id}')
async def add_dislike(post_id: int, user: UserType, session: SessionDep):
    """
    Add dislike to post
    :param post_id: id of a post
    :param user: current user
    :param session:
    :return:
    """
    CRUD(session).add_like(user.name, post_id, False)
    return {'status': 'ok'}


@router.post('/add_comment/{post_id}')
async def add_comment(post_id: int,
                      comment: CommentSchema,
                      user: UserType,
                      session: SessionDep):
    """
    Add a comment to a post
    :param post_id: id of a post
    :param comment: comment
    :param user: current user
    :param session:
    :return:
    """
    CRUD(session).add_comment(user.name, post_id, comment.comment)
    return {'status': 'ok'}


@router.get('/{post_id}', response_model=PostSchema)
def get_post_info(post_id: int, user: UserType, session: SessionDep):
    """
    get additional info about post
    :param post_id: id of a post
    :param user: current user
    :param session:
    :return:
    """
    return CRUD(session).get_post_info(post_id)
