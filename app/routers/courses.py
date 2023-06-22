import models
import schemas
import utils
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter(
    prefix='/courses',
    tags=['Courses']
)


@router.get('/', response_model=list[schemas.Course])
def get_all_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    return courses


@router.get('/{course_code}', response_model=schemas.Course)
def get_course(course_code: str, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(
        models.Course.course_code == course_code).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Course not found')

    return course


@router.post('/', response_model=schemas.Course)
def create_course(request: schemas.Course, db: Session = Depends(get_db)):
    course_by_code = db.query(models.Course).filter(
        models.Course.course_code == request.course_code).first()

    course_by_name = db.query(models.Course).filter(
        models.Course.course_name == request.course_name).first()

    if course_by_code or course_by_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Course already registered')

    elective_name = request.elective_name.lower()
    elective_name = "-".join(elective_name.split())

    new_course = models.Course(
        course_code=request.course_code,
        offered_by=request.offered_by,
        course_name=request.course_name,
        capacity=request.capacity,
        elective_name=elective_name
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


@router.delete('/{course_code}', status_code=status.HTTP_204_NO_CONTENT)
def delete_Course(course_code: str, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(
        models.Course.course_code == course_code).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Course not found')

    db.delete(course)
    db.commit()

    return 'Course deleted'
