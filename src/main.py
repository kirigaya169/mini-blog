from fastapi import FastAPI
from routes import auth_router, posts_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(posts_router)
