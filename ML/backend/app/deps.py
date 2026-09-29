from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from .database import get_db
from .models import Student
from .security import decode_token

bearer = HTTPBearer(auto_error=False)
def current_student(credentials: HTTPAuthorizationCredentials | None = Depends(bearer), db: Session = Depends(get_db)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Sign in to continue")
    student_id = decode_token(credentials.credentials)
    if not student_id:
        raise HTTPException(status_code=401, detail="Your session has expired. Please sign in again.")
    student = db.scalar(select(Student).where(Student.student_id == student_id))
    if not student:
        raise HTTPException(status_code=401, detail="Student account was not found")
    return student
