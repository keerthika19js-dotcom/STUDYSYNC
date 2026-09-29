from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import current_student
from ..models import Feedback, Student
from ..schemas import FeedbackInput

router = APIRouter()
@router.post("", status_code=201)
def create_feedback(payload: FeedbackInput, student: Student = Depends(current_student), db: Session = Depends(get_db)):
    if payload.partner_id == student.student_id: raise HTTPException(status_code=400, detail="You cannot leave feedback for yourself")
    db.add(Feedback(student_id=student.student_id, partner_id=payload.partner_id, useful=payload.useful, rating=payload.rating, comment=payload.comment.strip()))
    db.commit()
    return {"message": "Thanks — your feedback was saved."}
