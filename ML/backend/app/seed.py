import random
import csv
from pathlib import Path
from sqlalchemy import select
from .database import Base, engine, SessionLocal
from .models import Student
from .security import hash_password

NAMES = ["Aarav Mehta", "Mira Patel", "Ishaan Rao", "Anaya Shah", "Kabir Nair", "Zoya Khan", "Arjun Das", "Ira Menon", "Dev Kapoor", "Riya Bose", "Neil Thomas", "Sara Iyer", "Vivaan Jain", "Tara Sen", "Rehan Ali", "Aditi Roy", "Kian D'Souza", "Myra Gupta", "Rohan Pillai", "Diya Joshi", "Advik Sethi", "Nisha Verma", "Samar Reddy", "Kiara Malhotra", "Yash Kulkarni", "Aanya Fernandes", "Om Prakash", "Meera Krishnan", "Dhruv Bhat", "Sana Qureshi", "Parth Ghosh", "Lavanya Rao", "Ayaan Sheikh", "Pia Chatterjee", "Manav Soni", "Ishita Paul", "Ritvik Naidu", "Veda Mishra", "Atharv Bansal", "Navya Mathew", "Rudra Sen", "Sia Arora", "Kartik Shetty", "Aisha Mir", "Shaurya Roy", "Tanvi Desai", "Eshan Varma", "Rhea Lal", "Aditya Menon"]

def export_demo_csv(db):
    fields = ["student_id", "name", "department", "year", "python_score", "mathematics_score", "dbms_score", "ai_score", "study_hours", "study_frequency", "learning_pace", "learning_style", "communication_style", "preferred_study_time", "available_days", "study_goal", "data_type"]
    demo_students = db.scalars(select(Student).where(Student.student_id.between("S001", "S050")).order_by(Student.student_id)).all()
    path = Path(__file__).resolve().parents[2] / "data" / "students.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for student in demo_students:
            writer.writerow({field: getattr(student, field) for field in fields if field != "data_type"} | {"data_type": "DEMO/SIMULATED"})

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.scalar(select(Student.id).limit(1)) is not None:
            export_demo_csv(db)
            return
        rng = random.Random(42)
        styles = ["Visual", "Auditory", "Reading/Writing", "Kinesthetic"]
        goals = ["Exam Preparation", "Assignment", "Coding Practice", "Project Work", "Revision", "General Study"]
        days = ["Monday,Wednesday,Friday", "Tuesday,Thursday,Saturday", "Monday,Tuesday,Thursday", "Wednesday,Friday,Saturday", "Monday,Wednesday,Sunday"]
        patterns = [("python_score", "mathematics_score"), ("mathematics_score", "python_score"), ("dbms_score", "ai_score"), ("ai_score", "dbms_score")]
        accounts = [dict(student_id="S001", name="Demo Student", email="demo@studysync.com", password_hash=hash_password("demo123"), python_score=91, mathematics_score=52, dbms_score=78, ai_score=67, study_hours=3.0, study_frequency="4-5 days", learning_pace="Balanced", learning_style="Visual", communication_style="Collaborative", preferred_study_time="Evening", available_days="Monday,Wednesday,Friday", study_goal="Exam Preparation")]
        for i, name in enumerate(NAMES, 2):
            scores = {key: rng.randint(42, 91) for key in ("python_score", "mathematics_score", "dbms_score", "ai_score")}
            weak, strong = patterns[(i - 2) % len(patterns)]
            scores[weak], scores[strong] = rng.randint(43, 58), rng.randint(78, 96)
            accounts.append(dict(student_id=f"S{i:03d}", name=name, email=f"student{i}@studysync.demo", password_hash=hash_password("student123"), **scores, study_hours=round(rng.uniform(1, 6), 1), study_frequency=rng.choice(["1-2 days", "3 days", "4-5 days", "Daily"]), learning_pace=rng.choice(["Steady", "Balanced", "Fast"]), learning_style=rng.choice(styles), communication_style=rng.choice(["Collaborative", "Focused", "Discussion-led"]), preferred_study_time=rng.choice(["Morning", "Afternoon", "Evening", "Night"]), available_days=rng.choice(days), study_goal=rng.choice(goals)))
        for index, data in enumerate(accounts):
            db.add(Student(department=rng.choice(["Computer Science", "Information Technology", "Data Science"]), year=rng.randint(1, 4), **data))
        db.commit()
        export_demo_csv(db)
    finally: db.close()

if __name__ == "__main__":
    seed_database()
    print("Seeded 50 DEMO/SIMULATED student accounts. Demo login: demo@studysync.com / demo123")
