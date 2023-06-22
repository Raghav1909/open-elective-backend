import schemas
import models
import utils
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db

router = APIRouter(
    prefix='/students',
    tags=['Students']
)


@router.get('/', response_model=list[schemas.StudentOut])
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()

    return students


@router.get('/{USN}', response_model=schemas.StudentOut)
def get_student(USN: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(
        models.Student.USN == USN).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Student not found')

    return student


@router.post('/', response_model=schemas.StudentOut)
def create_student(request: schemas.StudentCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(
        models.Student.USN == request.USN).first()

    if student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='USN already registered')

    if request.USN[0:5] != "01JST":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid USN')

    new_student = models.Student(
        USN=request.USN,
        first_name=request.first_name,
        last_name=request.last_name,
        contact=request.contact,
        email=request.email,
        year=request.year,
        branch="CS",
        CGPA=request.CGPA,
        isStaff=False,
        password=utils.hash(request.password)
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@router.put('/{USN}', response_model=schemas.StudentOut)
def update_student(USN: str, request: schemas.StudentIn, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(
        models.Student.USN == USN).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Student not found')

    student.USN = request.USN
    student.first_name = request.first_name
    student.contact = request.contact
    student.email = request.email
    student.year = request.year
    student.branch = request.branch
    student.password = utils.hash(request.password)

    db.commit()
    db.refresh(student)
    return student


@router.delete('/{USN}', response_model=schemas.Student)
def delete_student(USN: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(
        models.Student.USN == USN).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Student not found')

    db.delete(student)
    db.commit()
    return student
