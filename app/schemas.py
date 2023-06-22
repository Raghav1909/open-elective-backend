from pydantic import BaseModel, EmailStr
from datetime import date


class User(BaseModel):
    first_name: str
    last_name: str
    contact: str
    email: str

    class Config:
        orm_mode = True


class Student(User):
    USN: str
    year: int
    CGPA: float


class StudentCreate(Student):
    password: str


class StudentOut(Student):
    isStaff: bool


class StudentIn(BaseModel):
    USN: str
    password: str


class Staff(User):
    username: str


class StaffCreate(Staff):
    password: str


class StaffOut(Staff):
    isStaff: bool


class StaffIn(BaseModel):
    username: str
    password: str


class Elective(BaseModel):
    elective_name: str

    class Config:
        orm_mode = True


class ElectiveCreate(Elective):
    pass


class Course(BaseModel):
    course_code: str
    offered_by: str
    course_name: str
    capacity: int
    elective_name: str

    class Config:
        orm_mode = True


class Response(BaseModel):
    USN: str
    elective_name: str
    preferences: list[str]
    alloted: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    email: EmailStr
