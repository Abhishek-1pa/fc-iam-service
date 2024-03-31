from fastapi import APIRouter, Depends, status , HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError
from .. import database, models, utils, schemas, oauth2
from typing import Type

router = APIRouter(
    
    tags=['Authentication']
    
)

@router.post('/login', response_model=schemas.LoginResponse)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):
    if user_credentials.username != "anchalshivank@example.com":
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f'You cannot login with this username')
    user:models.User or None = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")
    if utils.verify(user_credentials.password, user.password) is not True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Invalid credentials')
    token_data = {"id":user.id}
    access_token = oauth2.create_access_token(token_data)
    login_response = schemas.LoginResponse(
        id=user.id, 
        username=user.username, 
        email=user.email, 
        token = access_token, 
        token_type = "bearer",
        refresh_token = oauth2.create_refresh_token(token_data)
        )
    
    return login_response


@router.post('/refresh_token', response_model = schemas.LoginResponse)
async def refresh_token(refresh_token : str = Depends(utils.get_refresh_token), db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials', headers={'WWW-Authenticate':'Bearer'})

    token_data = oauth2.verify_access_token(refresh_token, credentials_exception=credentials_exception, db=db)
    user : Type[models.User] | None = db.query(models.User).filter(models.User.id == token_data.user_id).first()
    
    access_token = oauth2.create_access_token({"id":token_data.user_id})
    login_response = schemas.LoginResponse(
        id = user.id,
        username = user.username,
        email = user.email,
        token = access_token,
        token_type = "bearer",
        refresh_token = refresh_token
    )
    return login_response


@router.post('/get_current_user', response_model=schemas.UserCreated)
async def fetch_current_user(current_user :Type[models.User] | None= Depends(oauth2.get_current_user))->Type[models.User] | None:
    return current_user


