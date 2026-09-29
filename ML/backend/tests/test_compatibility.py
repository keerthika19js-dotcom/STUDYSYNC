from types import SimpleNamespace
from app.ml.compatibility import calculate_compatibility, complementary_analysis

def student(**overrides):
    data = dict(student_id="A", name="A", python_score=90, mathematics_score=52, dbms_score=80, ai_score=70, study_hours=3, study_frequency="4-5 days", learning_pace="Balanced", learning_style="Visual", communication_style="Collaborative", preferred_study_time="Evening", available_days="Monday,Wednesday,Friday", study_goal="Exam Preparation")
    data.update(overrides)
    return SimpleNamespace(**data)

def test_complementary_analysis_rewards_opposite_strengths():
    a = student()
    b = student(student_id="B", python_score=50, mathematics_score=88, dbms_score=55, ai_score=82)
    score, pairs, reasons = complementary_analysis(a, b)
    assert score == 100
    assert len(pairs) >= 2
    assert any("Mathematics" in reason for reason in reasons)
    assert any("Python" in reason for reason in reasons)

def test_identical_high_scores_do_not_get_complementarity_credit():
    a = student(python_score=91, mathematics_score=82, dbms_score=80, ai_score=75)
    b = student(student_id="B", python_score=91, mathematics_score=82, dbms_score=80, ai_score=75)
    assert complementary_analysis(a, b)[0] == 0

def test_reciprocal_skill_support_outranks_one_way_support():
    one_way_a = student(python_score=52, mathematics_score=65, dbms_score=65, ai_score=65)
    one_way_b = student(student_id="B", python_score=86, mathematics_score=65, dbms_score=65, ai_score=65)
    reciprocal_a = student(python_score=52, mathematics_score=88, dbms_score=65, ai_score=65)
    reciprocal_b = student(student_id="C", python_score=86, mathematics_score=52, dbms_score=65, ai_score=65)
    assert complementary_analysis(one_way_a, one_way_b)[0] == 50
    assert complementary_analysis(reciprocal_a, reciprocal_b)[0] == 100

def test_compatibility_is_bounded_and_dynamic():
    a = student()
    b = student(student_id="B", python_score=50, mathematics_score=88, dbms_score=55, ai_score=82)
    compatible = calculate_compatibility(a, b)
    changed = calculate_compatibility(a, student(student_id="C", preferred_study_time="Morning", available_days="Sunday", study_goal="Revision"))
    assert 0 <= compatible["compatibility_score"] <= 100
    assert compatible["compatibility_score"] != changed["compatibility_score"]
    assert compatible["complementary_score"] == 100
