from types import SimpleNamespace
from app.ml.recommender import rank_recommendations

def make(student_id, name, **kw):
    data=dict(student_id=student_id,name=name,department="Computer Science",year=2,python_score=60,mathematics_score=60,dbms_score=60,ai_score=60,study_hours=2,study_frequency="4-5 days",learning_pace="Balanced",learning_style="Visual",communication_style="Collaborative",preferred_study_time="Evening",available_days="Monday,Wednesday,Friday",study_goal="Exam Preparation")
    data.update(kw)
    return SimpleNamespace(**data)

def test_recommendations_exclude_self_and_rank_highest_first():
    students=[make("A","A",python_score=90,mathematics_score=50),make("B","B",python_score=50,mathematics_score=90),make("C","C",python_score=55,mathematics_score=52,preferred_study_time="Night",study_goal="Revision"),make("D","D")]
    results=rank_recommendations(students,"A",5)
    assert len(results)==3
    assert all(r["student_id"]!="A" for r in results)
    assert results[0]["student_id"]=="B"
    assert [r["compatibility_score"] for r in results]==sorted([r["compatibility_score"] for r in results],reverse=True)
    assert "reasons" in results[0] and results[0]["complementary_score"] > 0
