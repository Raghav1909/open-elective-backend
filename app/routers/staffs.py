import models
import schemas
import utils
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter(
    prefix='/staffs',
    tags=['Staffs']
)


@router.get('/', response_model=list[schemas.StaffOut])
def get_all_staffs(db: Session = Depends(get_db)):
    staffs = db.query(models.Staff).all()

    return staffs


@router.get('/{username}', response_model=schemas.StaffOut)
def get_staff(username: str, db: Session = Depends(get_db)):
    staff = db.query(models.Staff).filter(
        models.Staff.username == username).first()

    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='staff not found')

    return staff


@router.post('/', response_model=schemas.StaffOut)
def create_staff(request: schemas.StaffCreate, db: Session = Depends(get_db)):
    user = db.query(models.Staff).filter(
        models.Staff.username == request.username).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Username already registered')

    new_user = models.Staff(
        first_name=request.first_name,
        last_name=request.last_name,
        contact=request.contact,
        email=request.email,
        username=request.username,
        password=utils.hash(request.password),
        isStaff=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.delete('/{username}', status_code=status.HTTP_204_NO_CONTENT)
def delete_staff(username: str, db: Session = Depends(get_db)):
    staff = db.query(models.Staff).filter(
        models.Staff.username == username).first()

    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Staff not found')

    db.delete(staff)
    db.commit()

    return 'Staff deleted'


@router.put('/{username}', status_code=status.HTTP_202_ACCEPTED)
def update_staff(username: str, request: schemas.StaffIn, db: Session = Depends(get_db)):
    admin = db.query(models.Staff).filter(
        models.Staff.username == username).first()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Staff not found')

    admin.password = utils.hash(request.password)
    db.commit()

    return 'Staff updated'


@router.delete('/{username}', status_code=status.HTTP_204_NO_CONTENT)
def delete_staff(username: str, db: Session = Depends(get_db)):
    staff = db.query(models.Staff).filter(
        models.Staff.username == username).first()

    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Staff not found')

    db.delete(staff)
    db.commit()

    return 'Staff deleted'
