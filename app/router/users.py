from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app import schemas, database, models, util, oauth2
from app.schemas import Post, PostCreate
from app.util import hash_password, pwd_context

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    new_user.password = hash_password(user.password)
    db = next(get_db())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
