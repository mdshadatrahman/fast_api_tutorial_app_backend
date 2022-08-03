from fastapi import APIRouter, Depends, status, HTTPException, APIRouter
from requests import Session
import models
import schemas
import utils
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    test_use = db.query(models.User).filter(
        models.User.email == user.email).first()

    if test_use:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"email ({user.email}) already exists")

    # hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} not found")

    return user
