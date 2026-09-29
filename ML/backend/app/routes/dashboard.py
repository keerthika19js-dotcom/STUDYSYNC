from collections import Counter
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import current_student
from ..models import Feedback, MatchEvent, Student
from ..ml.clustering import StudentClusterer
from ..ml.recommender import rank_recommendations

router = APIRouter()
@router.get("")
def dashboard(current: Student = Depends(current_student), db: Session = Depends(get_db)):
    students = list(db.scalars(select(Student).order_by(Student.student_id)).all())
    recs = rank_recommendations(students, current.student_id, 5, StudentClusterer().fit(students)) if len(students) > 1 else []
    return {"total_students": len(students), "potential_partners": max(0, len(students)-1), "best_compatibility": recs[0]["compatibility_score"] if recs else 0, "average_compatibility": round(sum(r["compatibility_score"] for r in recs)/len(recs)) if recs else 0, "goal_distribution": dict(Counter(s.study_goal for s in students)), "learning_style_distribution": dict(Counter(s.learning_style for s in students)), "top_matches": recs[:3], "feedback_count": db.scalar(select(func.count()).select_from(Feedback)) or 0, "matches_generated": db.scalar(select(func.count()).select_from(MatchEvent)) or 0}
