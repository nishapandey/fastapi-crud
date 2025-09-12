from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import schemas
from .schemas import Post, PostCreate
# from .util import hash_password  # Removed due to missing definition
from .util import hash_password, pwd_context  # Added import for pwd_context
from .router import posts, users, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
