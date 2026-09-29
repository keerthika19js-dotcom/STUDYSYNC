from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import current_student
from ..models import Student
from ..schemas import ProfileUpdate, StudentProfile

router = APIRouter()
@router.get("/me", response_model=StudentProfile)
def me(student: Student = Depends(current_student)):
    return student

@router.put("/me", response_model=StudentProfile)
def update_me(payload: ProfileUpdate, student: Student = Depends(current_student), db: Session = Depends(get_db)):
    for key, value in payload.model_dump().items(): setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return student

@router.get("/{student_id}", response_model=StudentProfile)
def get_student(student_id: str, _: Student = Depends(current_student), db: Session = Depends(get_db)):
    result = db.scalar(select(Student).where(Student.student_id == student_id))
    if not result: raise HTTPException(status_code=404, detail="Student was not found")
    return result
