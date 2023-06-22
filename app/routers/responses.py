import models
import schemas
import utils
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter(
    prefix='/responses',
    tags=['Responses']
)


@router.get('/', response_model=schemas.Response)
def get_responses(db: Session = Depends(get_db)):
    responses = db.query(models.Response).all()
    return responses

@router.post('/')
def create_response(request: schemas.Response , db: Session = Depends(get_db)):
    response =  db.query(models.Response).filter(
        models.Response.USN == request.USN).filter(models.Response.elective_name == request.elective_name).first()
    if response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Response already given')

    new_response = models.Response(
        USN = request.USN,
        elective_name = request.elective_name,
        first_preference = request.preferences[0],
        second_preference = request.preferences[1],
        third_preference = request.preferences[2],
        fourth_preference = request.preferences[3],
        fifth_preference = request.preferences[4],
        sixth_preference = request.preferences[5],
        seventh_preference = request.preferences[6],
        eighth_preference = request.preferences[7],
        ninth_preference = request.preferences[8],
        tenth_preference = request.preferences[9]
    )

    db.add(new_response)
    db.commit()
    db.refresh(new_response)
    return new_response
    