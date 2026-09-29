from datetime import datetime, timezone
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[str] = mapped_column(String(16), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(256))
    department: Mapped[str] = mapped_column(String(80), default="Computer Science")
    year: Mapped[int] = mapped_column(Integer, default=2)
    python_score: Mapped[float] = mapped_column(Float, default=70)
    mathematics_score: Mapped[float] = mapped_column(Float, default=70)
    dbms_score: Mapped[float] = mapped_column(Float, default=70)
    ai_score: Mapped[float] = mapped_column(Float, default=70)
    study_hours: Mapped[float] = mapped_column(Float, default=2)
    study_frequency: Mapped[str] = mapped_column(String(32), default="4-5 days")
    learning_pace: Mapped[str] = mapped_column(String(32), default="Balanced")
    learning_style: Mapped[str] = mapped_column(String(32), default="Visual")
    communication_style: Mapped[str] = mapped_column(String(32), default="Collaborative")
    preferred_study_time: Mapped[str] = mapped_column(String(32), default="Evening")
    available_days: Mapped[str] = mapped_column(String(120), default="Monday,Wednesday,Friday")
    study_goal: Mapped[str] = mapped_column(String(48), default="Exam Preparation")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class Feedback(Base):
    __tablename__ = "feedback"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[str] = mapped_column(ForeignKey("students.student_id"), index=True)
    partner_id: Mapped[str] = mapped_column(ForeignKey("students.student_id"))
    useful: Mapped[bool] = mapped_column()
    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

class MatchEvent(Base):
    __tablename__ = "match_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[str] = mapped_column(ForeignKey("students.student_id"), index=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    result_count: Mapped[int] = mapped_column(Integer, default=0)
