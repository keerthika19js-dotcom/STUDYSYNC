from collections import Counter
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import current_student
from ..models import Feedback, MatchEvent, Student
from ..ml.clustering import StudentClusterer
from ..ml.compatibility import WEIGHTS
from ..ml.recommender import rank_recommendations

router = APIRouter()
@router.get("/clusters")
def clusters(_: Student = Depends(current_student), db: Session = Depends(get_db)):
    students = list(db.scalars(select(Student).order_by(Student.student_id)).all())
    model = StudentClusterer().fit(students)
    counts = Counter(model.labels.values())
    return {"clusters": [{"cluster": i, "label": f"Cluster {i+1}", "students": count} for i, count in sorted(counts.items())], "student_clusters": model.labels, "student_count": len(students), "algorithm": "K-Means (k = min(4, student count), random_state=42)"}

@router.post("/run")
def run_pipeline(_: Student = Depends(current_student), db: Session = Depends(get_db)):
    students = list(db.scalars(select(Student).order_by(Student.student_id)).all())
    model = StudentClusterer().fit(students)
    return {"message": "ML pipeline retrained successfully using current database profiles.", "students_processed": len(students), "clusters": len(set(model.labels.values())), "algorithm": "K-Means", "weights": WEIGHTS}

@router.get("/insights")
def insights(student: Student = Depends(current_student), db: Session = Depends(get_db)):
    students = list(db.scalars(select(Student).order_by(Student.student_id)).all())
    model = StudentClusterer().fit(students)
    recommendations = rank_recommendations(students, student.student_id, 5, model) if len(students) > 1 else []
    average_compatibility = round(sum(match["compatibility_score"] for match in recommendations) / len(recommendations)) if recommendations else 0
    return {"clusters": [{"cluster": i, "label": f"Cluster {i+1}", "students": count} for i, count in sorted(Counter(model.labels.values()).items())], "weights": WEIGHTS, "student_count": len(students), "matches_generated": db.scalar(select(func.count()).select_from(MatchEvent)) or 0, "average_compatibility": average_compatibility, "feedback_count": db.scalar(select(func.count()).select_from(Feedback)) or 0}
