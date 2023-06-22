import models
import schemas
import utils
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter(
    prefix='/electives',
    tags=['Electives']
)


@router.get('/', response_model=list[schemas.Elective])
def get_all_electives(db: Session = Depends(get_db)):
    electives = db.query(models.Elective).all()

    for elective in electives:
        elective.elective_name = " ".join(elective.elective_name.split('-'))
        elective.elective_name = elective.elective_name.title()

    return electives


@router.get('/{elective_name}/allotment')
def allotment(elective_name: str, db: Session = Depends(get_db)):
    pass


@router.get('/{elective_name}/courses', response_model=list[schemas.Course])
def get_courses_of_elective(elective_name: str, db: Session = Depends(get_db)):
    courses = db.query(models.Course).filter(
        models.Course.elective_name == elective_name).all()

    return courses


@router.get('/{elective_name}', response_model=schemas.Elective)
def get_elective(elective_name: str, db: Session = Depends(get_db)):
    elective = db.query(models.Elective).filter(
        models.Elective.elective_name == elective_name).first()

    if not elective:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Elective not found')

    elective.elective_name = " ".join(elective.elective_name.split('-'))
    elective.elective_name = elective.elective_name.title()

    return elective


@router.post('/', response_model=schemas.Elective)
def create_elective(request: schemas.ElectiveCreate, db: Session = Depends(get_db)):
    elective = db.query(models.Elective).filter(
        models.Elective.elective_name == request.elective_name).first()

    if elective:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Elective already registered')

    elective_name = request.elective_name.lower()
    elective_name = "-".join(elective_name.split())
    new_elective = models.Elective(
        elective_name=elective_name,
    )

    db.add(new_elective)
    db.commit()
    db.refresh(new_elective)
    return new_elective


# @router.post("/{username}/profile_photo",status_code=status.HTTP_200_OK)
# def create_or_update_elective_pdf(username: str,file: UploadFile = File(...), db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
#     if username != current_user.username and current_user.is_superuser == False:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to create/update profile photo")

#     db_user = db.query(models.User).filter(models.User.username == username).first()
#     if db_user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#     db_profile_photo = db.query(models.ProfilePhoto).filter(models.ProfilePhoto.username == username).first()
#     id = -1
#     if db_profile_photo:
#         id = db_profile_photo.id
#         db.delete(db_profile_photo)
#         db.commit()
#         os.remove(f"static/profile_photos/{db_profile_photo.img_name}")

#     file_name = secrets.token_hex(8)
#     file_extension = file.filename.split(".")[-1]

#     if file_extension.lower() not in ("png", "jpg", "jpeg"):
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")
#     file_name = f"{file_name}.{file_extension}"
#     with open(f"static/profile_photos/{file_name}", "wb") as buffer:
#         image = Image.open(file.file)
#         image = image.resize((200,200))
#         if file_extension.lower() == "png":
#             image.save(buffer, format="PNG")
#         if file_extension.lower() == "jpg" or file_extension.lower() == "jpeg":
#             image.save(buffer, format="JPEG")

#     if id == - 1:
#         new_profile_photo = models.ProfilePhoto(username = username,img_name = file_name)
#     else:
#         new_profile_photo = models.ProfilePhoto(id = id,username = username,img_name = file_name)
#     db.add(new_profile_photo)
#     db.commit()
#     db.refresh(new_profile_photo)
#     return Response(status_code=status.HTTP_201_CREATED)

@router.delete('/{elective_name}', status_code=status.HTTP_204_NO_CONTENT)
def delete_elective(elective_name: str, db: Session = Depends(get_db)):
    elective = db.query(models.Elective).filter(
        models.Elective.elective_name == elective_name).first()

    if not elective:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Elective not found')

    db.delete(elective)
    db.commit()

    return 'Elective deleted'
