from fastapi import APIRouter, status, Depends, HTTPException

from .. import database, schemas, models, utils
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user",
    tags = ["User"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreated)
def create_user(user:schemas.UserCreate, db: Session = Depends(database.get_db)):
    try:
        exists = db.query(models.User).filter(models.User.email == user.email).first()
        if exists is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User with this email already exists')
        hashed_pwd = utils.hash(user.password)
        user.password = hashed_pwd
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except HTTPException as http_exception:
        # Handle specific HTTP exceptions
        raise http_exception

    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail="Internal server error")