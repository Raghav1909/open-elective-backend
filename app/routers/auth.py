from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

import schemas
import models
import utils
import oauth2
from database import get_db

router = APIRouter(tags=['Authentication'])


@router.post('/auth', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    if user_credentials.username[0:5] == '01JST':
        user = db.query(models.Student).filter(
            models.Student.USN == user_credentials.username).first()
    else:
        user = db.query(models.Staff).filter(
            models.Staff.username == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')

    if user_credentials.username[0:5] == '01JST':
        access_token = oauth2.create_access_token(
            data={'USN': user.USN})
    else:
        access_token = oauth2.create_access_token(
            data={'username': user.username})

    return {'access_token': access_token, 'token_type': 'bearer'}
