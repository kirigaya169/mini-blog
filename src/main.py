from fastapi import FastAPI, Depends
from utils.auth.get_user import get_current_user
from utils.db_session import db_session_dependency
from schemas import UserSchema
from typing import Annotated
from sqlalchemy.orm import Session
app = FastAPI()
