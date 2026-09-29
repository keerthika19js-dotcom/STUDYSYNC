from .similarity import cosine_score

WEIGHTS = {"academic": .30, "complementary": .30, "availability": .15, "learning_style": .10, "behavior": .05, "goal": .10}
SUBJECTS = {"python_score": "Python", "mathematics_score": "Mathematics", "dbms_score": "DBMS", "ai_score": "AI"}

def value(student, key):
    return student.get(key) if isinstance(student, dict) else getattr(student, key)

def complementary_analysis(a, b):
    pairs, reasons = [], []
    for key, label in SUBJECTS.items():
        av, bv = float(value(a, key)), float(value(b, key))
        if av < 60 and bv >= 75:
            pairs.append({"learner": "you", "mentor": "partner", "subject": label})
            reasons.append(f"They are strong in {label}, where you can use support")
        if bv < 60 and av >= 75:
            pairs.append({"learner": "partner", "mentor": "you", "subject": label})
            reasons.append(f"You are strong in {label}, where they can use support")
    # Reciprocal teaching support outranks one-way tutoring, even when a student has several strong subjects.
    directions = {pair["learner"] for pair in pairs}
    if not pairs:
        score = 0.0
    elif len(directions) == 2:
        score = 100.0
    else:
        score = min(75.0, 50.0 + max(0, len(pairs) - 1) * 12.5)
    return score, pairs, reasons

def availability_score(a, b):
    days_a = {d.strip().lower() for d in value(a, "available_days").split(",") if d.strip()}
    days_b = {d.strip().lower() for d in value(b, "available_days").split(",") if d.strip()}
    overlap = len(days_a & days_b) / max(1, len(days_a | days_b))
    time_a, time_b = value(a, "preferred_study_time"), value(b, "preferred_study_time")
    time_score = 1.0 if time_a == time_b else (.5 if {time_a, time_b} <= {"Morning", "Afternoon"} or {time_a, time_b} <= {"Afternoon", "Evening"} else 0.0)
    return (overlap * .65 + time_score * .35) * 100

def learning_score(a, b):
    left, right = value(a, "learning_style"), value(b, "learning_style")
    if left == right: return 88.0
    pairs = {frozenset(("Visual", "Reading/Writing")): 82, frozenset(("Auditory", "Kinesthetic")): 76, frozenset(("Visual", "Kinesthetic")): 72}
    return float(pairs.get(frozenset((left, right)), 62))

def academic_score(a, b, vector_a=None, vector_b=None):
    keys = list(SUBJECTS)
    av = [float(value(a, k)) for k in keys]
    bv = [float(value(b, k)) for k in keys]
    similarity = cosine_score(av, bv) if vector_a is None or vector_b is None else cosine_score(vector_a, vector_b)
    # Cosine similarity captures shared academic range; moderate score-distance tolerance encourages peer-level study.
    distance = sum(abs(x-y) for x, y in zip(av, bv)) / (len(av) * 100)
    return max(0.0, min(100.0, similarity * 65 + (1-distance) * 35))

def behavior_score(a, b, same_cluster=False):
    hours = max(0.0, 100 - abs(float(value(a, "study_hours")) - float(value(b, "study_hours"))) * 12)
    frequency = 100 if value(a, "study_frequency") == value(b, "study_frequency") else 55
    pace = 100 if value(a, "learning_pace") == value(b, "learning_pace") else 65
    communication = 100 if value(a, "communication_style") == value(b, "communication_style") else 70
    return min(100.0, (hours + frequency + pace + communication) / 4 + (5 if same_cluster else 0))

def calculate_compatibility(a, b, same_cluster=False, vectors=None):
    academic = academic_score(a, b, *(vectors or (None, None)))
    complementary, pairs, complement_reasons = complementary_analysis(a, b)
    availability = availability_score(a, b)
    learning = learning_score(a, b)
    behavior = behavior_score(a, b, same_cluster)
    goal = 100.0 if value(a, "study_goal") == value(b, "study_goal") else (55.0 if value(a, "study_goal") in {"Assignment", "Project Work", "Coding Practice"} and value(b, "study_goal") in {"Assignment", "Project Work", "Coding Practice"} else 30.0)
    components = {"academic_score": round(academic), "complementary_score": round(complementary), "availability_score": round(availability), "learning_style_score": round(learning), "behavior_score": round(behavior), "goal_score": round(goal)}
    score = sum(components[f"{name}_score"] * weight for name, weight in WEIGHTS.items())
    reasons = list(complement_reasons)
    if availability >= 70: reasons.append("Your study schedules overlap")
    if value(a, "preferred_study_time") == value(b, "preferred_study_time"): reasons.append(f"Both prefer {value(a, 'preferred_study_time').lower()} study")
    if goal >= 90: reasons.append(f"Both are focused on {value(a, 'study_goal').lower()}")
    if learning >= 80: reasons.append("Your learning styles work well together")
    if not reasons: reasons.append("Your study habits and academic profiles are a promising fit")
    return {"compatibility_score": round(max(0, min(100, score))), **components, "reasons": reasons, "complementary_pairs": pairs}
