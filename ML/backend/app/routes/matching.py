from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import current_student
from ..models import MatchEvent, Student
from ..ml.clustering import StudentClusterer
from ..ml.recommender import rank_recommendations

router = APIRouter()
@router.get("/recommendations/{student_id}")
def recommendations(student_id: str, current: Student = Depends(current_student), db: Session = Depends(get_db)):
    if current.student_id != student_id:
        raise HTTPException(status_code=403, detail="You can only request recommendations for your own profile")
    students = list(db.scalars(select(Student).order_by(Student.student_id)).all())
    if len(students) < 2: return {"student_id": student_id, "recommendations": [], "message": "Add more students to discover study partners."}
    model = StudentClusterer().fit(students)
    results = rank_recommendations(students, student_id, 5, model)
    db.add(MatchEvent(student_id=student_id, result_count=len(results)))
    db.commit()
    return {"student_id": student_id, "cluster": model.cluster_for(student_id), "recommendations": results}

@router.get("/{student_id}/{partner_id}")
def match_detail(student_id: str, partner_id: str, current: Student = Depends(current_student), db: Session = Depends(get_db)):
    if current.student_id != student_id: raise HTTPException(status_code=403, detail="You can only view your own match details")
    rows = list(db.scalars(select(Student).order_by(Student.student_id)).all())
    if not any(s.student_id == partner_id for s in rows): raise HTTPException(status_code=404, detail="Partner was not found")
    matches = rank_recommendations(rows, student_id, max(5, len(rows)), StudentClusterer().fit(rows))
    match = next((r for r in matches if r["student_id"] == partner_id), None)
    if not match: raise HTTPException(status_code=404, detail="Match details are unavailable")
    return {"student": {"student_id": current.student_id, "name": current.name, "profile": {k: getattr(current, k) for k in match["profile"]}}, "recommendation": match}
