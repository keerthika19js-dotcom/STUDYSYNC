from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Student
from ..schemas import LoginInput, RegisterInput
from ..security import create_token, hash_password, verify_password
from ..deps import current_student

router = APIRouter()
def auth_result(student):
    return {"access_token": create_token(student.student_id), "token_type": "bearer", "student": {"student_id": student.student_id, "name": student.name, "email": student.email}}

@router.post("/register", status_code=201)
def register(payload: RegisterInput, db: Session = Depends(get_db)):
    email = payload.email.lower()
    if db.scalar(select(Student).where(Student.email == email)):
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    number = (db.query(Student).count() + 1)
    student = Student(student_id=f"U{number:04d}", name=payload.name.strip(), email=email, password_hash=hash_password(payload.password))
    db.add(student)
    db.commit()
    db.refresh(student)
    return auth_result(student)

@router.post("/login")
def login(payload: LoginInput, db: Session = Depends(get_db)):
    student = db.scalar(select(Student).where(Student.email == payload.email.lower()))
    if not student or not verify_password(payload.password, student.password_hash):
        raise HTTPException(status_code=401, detail="Email or password is incorrect")
    return auth_result(student)

@router.post("/demo-login")
def demo_login(db: Session = Depends(get_db)):
    student = db.scalar(select(Student).where(Student.email == "demo@studysync.com"))
    if not student: raise HTTPException(status_code=503, detail="Demo account is not available. Run the seed script first.")
    return auth_result(student)

@router.post("/logout")
def logout(_: Student = Depends(current_student)):
    return {"message": "Signed out successfully"}
