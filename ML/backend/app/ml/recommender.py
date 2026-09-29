from sklearn.metrics.pairwise import cosine_similarity
from .preprocessing import transform_students
from .compatibility import calculate_compatibility
from .clustering import StudentClusterer

def rank_recommendations(students, student_id, limit=5, clusterer=None):
    by_id = {s.student_id: s for s in students}
    if student_id not in by_id:
        raise ValueError("Student not found")
    _, matrix, _ = transform_students(students)
    positions = {s.student_id: i for i, s in enumerate(students)}
    model = clusterer or StudentClusterer().fit(students)
    target = by_id[student_id]
    results = []
    for candidate in students:
        if candidate.student_id == student_id: continue
        same_cluster = model.cluster_for(student_id) == model.cluster_for(candidate.student_id)
        metrics = calculate_compatibility(target, candidate, same_cluster, (matrix[positions[student_id]], matrix[positions[candidate.student_id]]))
        cosine = max(0.0, min(1.0, float(cosine_similarity(matrix[positions[student_id]:positions[student_id]+1], matrix[positions[candidate.student_id]:positions[candidate.student_id]+1])[0, 0])))
        results.append({"student_id": candidate.student_id, "name": candidate.name, "department": candidate.department, "year": candidate.year, "cluster": model.cluster_for(candidate.student_id), "cosine_similarity": round(cosine, 4), "profile": {k: getattr(candidate, k) for k in ("python_score", "mathematics_score", "dbms_score", "ai_score", "study_hours", "study_frequency", "learning_pace", "learning_style", "communication_style", "preferred_study_time", "available_days", "study_goal")}, **metrics})
    return sorted(results, key=lambda r: (-r["compatibility_score"], -r["complementary_score"], r["name"]))[:limit]
