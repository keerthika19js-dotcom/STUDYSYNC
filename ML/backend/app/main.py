import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from .database import Base, engine
from .seed import seed_database
from .routes import auth, students, matching, feedback, dashboard, ml

app = FastAPI(title="STUDYSYNC API", description="AI-powered, explainable study partner matching using student profile data.", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(students.router, prefix="/api/students", tags=["Students"])
app.include_router(matching.router, prefix="/api/matching", tags=["Matching"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["Feedback"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(ml.router, prefix="/api/ml", tags=["ML Pipeline"])

@app.get("/", include_in_schema=False)
def frontend_home():
    """Send the backend root to the React app; Swagger remains at /docs."""
    frontend_url = os.getenv("STUDYSYNC_FRONTEND_URL", "http://127.0.0.1:5173/")
    return RedirectResponse(url=frontend_url)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    seed_database()

@app.get("/api/health", tags=["System"])
def health(): return {"status": "ok", "service": "STUDYSYNC"}
