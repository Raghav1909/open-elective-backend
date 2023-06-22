from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Double

from database import Base


class User(Base):
    __abstract__ = True

    password = Column(String)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    contact = Column(String)
    email = Column(String)
    isStaff = Column(Boolean)


class Staff(User):
    __tablename__ = 'staffs'

    username = Column(String, primary_key=True, unique=True, index=True)


class Student(User):
    __tablename__ = 'students'

    USN = Column(String, primary_key=True, unique=True, index=True)
    year = Column(Integer)
    branch = Column(String)
    CGPA = Column(Double, nullable=False)


class Elective(Base):
    __tablename__ = 'electives'

    elective_name = Column(String, primary_key=True, unique=True, index=True)
    syllabus_pdf = Column(String, nullable=True, unique=True)


class Course(Base):
    __tablename__ = 'courses'

    course_code = Column(String, primary_key=True, unique=True, index=True)
    offered_by = Column(String, nullable=False)
    course_name = Column(String, nullable=False, unique=True)
    capacity = Column(Integer, nullable=False)
    elective_name = Column(String, ForeignKey(
        "electives.elective_name"), nullable=False)


class Response(Base):
    __tablename__ = 'responses'

    id = Column(String, primary_key=True, unique=True, index=True)
    USN = Column(String, ForeignKey("students.USN"), nullable=True)
    elective_name = Column(String, ForeignKey(
        "electives.elective_name"), nullable=False)
    first_preference = Column(String, nullable=False)
    second_preference = Column(String, nullable=False)
    third_preference = Column(String, nullable=False)
    fourth_preference = Column(String, nullable=False)
    fifth_preference = Column(String, nullable=False)
    sixth_preference = Column(String, nullable=False)
    seventh_preference = Column(String, nullable=False)
    eighth_preference = Column(String, nullable=False)
    ninth_preference = Column(String, nullable=False)
    tenth_preference = Column(String, nullable=False)
    alloted = Column(String, nullable=True)
