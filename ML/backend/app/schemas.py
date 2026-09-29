from pydantic import BaseModel, ConfigDict, EmailStr, Field

class RegisterInput(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class LoginInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

class StudentProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    student_id: str
    name: str
    email: EmailStr
    department: str
    year: int
    python_score: float
    mathematics_score: float
    dbms_score: float
    ai_score: float
    study_hours: float
    study_frequency: str
    learning_pace: str
    learning_style: str
    communication_style: str
    preferred_study_time: str
    available_days: str
    study_goal: str

class ProfileUpdate(BaseModel):
    department: str = Field(min_length=2, max_length=80)
    year: int = Field(ge=1, le=8)
    python_score: float = Field(ge=0, le=100)
    mathematics_score: float = Field(ge=0, le=100)
    dbms_score: float = Field(ge=0, le=100)
    ai_score: float = Field(ge=0, le=100)
    study_hours: float = Field(ge=0, le=16)
    study_frequency: str
    learning_pace: str
    learning_style: str
    communication_style: str
    preferred_study_time: str
    available_days: str
    study_goal: str

class FeedbackInput(BaseModel):
    partner_id: str
    useful: bool
    rating: int = Field(ge=1, le=5)
    comment: str = Field(default="", max_length=1000)
