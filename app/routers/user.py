from typing import Optional, List
from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
#---------------------------------USERS---------------------------------------------
router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.UserResponse)
def create_user(user:schemas.UserCreate, db:Session = Depends(get_db)):

    #hash the pasword - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/all",response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db), limit: int | None = None):
    if limit is None:
        users = db.query(models.User).all()
    else:
        users = db.query(models.User).limit(limit).all()
    return users


@router.get("/{id}",response_model=schemas.UserResponse)
def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"User with id {id} does not exist")
    
    return user
