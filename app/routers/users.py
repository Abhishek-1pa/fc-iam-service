from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from .. import oauth2, schemas, database, models
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get('/{user_id}', response_model=schemas.UserCreated)
def get_user(user_id:int ,db:Session = Depends(database.get_db), current_user:models.User=Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id : {user_id} was not found')
    return user
@router.get('/', response_model=List[schemas.UserCreated])
def get_users(db:Session = Depends(database.get_db), current_user:models.User = Depends(oauth2.get_current_user)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Unable to fetch users')
    return users

 