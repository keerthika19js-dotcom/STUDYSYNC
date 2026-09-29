from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app

def test_health_and_demo_login():
    with TestClient(app) as client:
        assert client.get("/api/health").json()["status"] == "ok"
        response=client.post("/api/auth/login",json={"email":"demo@studysync.com","password":"demo123"})
        assert response.status_code==200
        token=response.json()["access_token"]
        headers={"Authorization":f"Bearer {token}"}
        profile=client.get("/api/students/me",headers=headers)
        assert profile.status_code==200
        assert "password_hash" not in profile.json()
        recommendations=client.get(f"/api/matching/recommendations/{profile.json()['student_id']}",headers=headers)
        assert recommendations.status_code==200
        assert len(recommendations.json()["recommendations"])==5
        insights=client.get("/api/ml/insights",headers=headers)
        assert 0<=insights.json()["average_compatibility"]<=100

def test_registration_and_validation():
    with TestClient(app) as client:
        response=client.post("/api/auth/register",json={"name":"Test Learner","email":f"test-user-{uuid4().hex}@studysync.demo","password":"valid-pass-123"})
        assert response.status_code==201
        assert response.json()["student"]["name"]=="Test Learner"
        invalid=client.post("/api/auth/register",json={"name":"X","email":"wrong","password":"tiny"})
        assert invalid.status_code==422

def test_profile_changes_recalculate_matches_and_feedback_is_saved():
    with TestClient(app) as client:
        login=client.post("/api/auth/demo-login")
        headers={"Authorization":f"Bearer {login.json()['access_token']}"}
        original=client.get("/api/students/me",headers=headers).json()
        profile={key:value for key,value in original.items() if key not in {"student_id","name","email"}}
        before=client.get(f"/api/matching/recommendations/{original['student_id']}",headers=headers).json()["recommendations"]
        altered={**profile,"preferred_study_time":"Morning","available_days":"Sunday"}
        assert client.put("/api/students/me",headers=headers,json=altered).status_code==200
        after=client.get(f"/api/matching/recommendations/{original['student_id']}",headers=headers).json()["recommendations"]
        try:
            before_scores={match["student_id"]:match["compatibility_score"] for match in before}
            after_scores={match["student_id"]:match["compatibility_score"] for match in after}
            assert any(before_scores[key]!=after_scores[key] for key in before_scores.keys() & after_scores.keys())
            assert client.post("/api/feedback",headers=headers,json={"partner_id":after[0]["student_id"],"useful":True,"rating":4,"comment":"Good complementary subject fit"}).status_code==201
            assert client.get("/api/dashboard",headers=headers).json()["feedback_count"]>=1
        finally:
            client.put("/api/students/me",headers=headers,json=profile)
