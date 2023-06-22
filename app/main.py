from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, students, staffs, electives, courses
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(staffs.router)
app.include_router(electives.router)
app.include_router(courses.router)


@app.get("/")
async def root():
    return "Open Elective Portal APIs"


@app.get("/departments")
async def get_all_departments():
    departments = [
        ("CSE", "Computer Science and Engineering"),
        ("ISE", "Information Science Engineering"),
        ("ECE", "Electronics and Communication Engineering"),
        ("CV", "Civil Engineering"),
        ("ME", "Mechanical Engineering"),
        ("EEE", "Electrical and Electronics Engineering"),
        ("EI", "Electronics and Instrumentation Engineering"),
        ("IP", "Industrial Production"),
        ("CSBS", "Computer Science and Business Systems Engineering"),
        ("CTM", "Construction Technology Management"),
        ("PST", "Polymer Science Engineering"),
        ("BT", "Biotechnology Engineering"),
        ("EV", "Environmental Engineering"),
    ]

    return departments
