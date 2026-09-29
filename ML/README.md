# STUDYSYNC — AI Study Partner Matcher

STUDYSYNC is a locally runnable, full-stack college ML project that recommends study partners based on academic performance, complementary skills, availability, learning preferences, study behaviour and goals. Match scores are computed from current SQLite profiles; results are not hardcoded.

**STUDYSYNC website:** [http://127.0.0.1:5173/](http://127.0.0.1:5173/) · **API docs for testing only:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Opening the backend root at `http://127.0.0.1:8000/` redirects to the frontend; keep both development servers running.

> **Demo data:** The 50 student profiles created by the seed script are deterministic DEMO/SIMULATED records. They are not real people. Demo login: `demo@studysync.com` / `demo123`.

## Features

- React + TypeScript + Vite responsive product UI with dashboard, profile editor, matching flow, side-by-side match details, ML insights and demo admin pages.
- FastAPI API with Swagger, registration, login, logout, profile updates, feedback, dashboard statistics and clustering endpoints.
- SQLite persistence with SQLAlchemy; passwords use salted PBKDF2-HMAC-SHA256 hashes.
- Real preprocessing using pandas, `ColumnTransformer`, `StandardScaler`, imputation and `OneHotEncoder`; reproducible K-Means clusters; cosine similarity; weighted ranking and profile-derived explanations.
- Reproducible cohort of 50 simulated students with deliberate opposite subject strengths to demonstrate tutoring complementarity.
- Every recommendation request re-reads profiles and recalculates features and rankings. Feedback is persisted for future evaluation.

## Architecture

```text
frontend (React/Vite) ── JSON + bearer token ──> FastAPI ── SQLAlchemy ──> SQLite
                                                   │
                         pandas → imputation/scaling/encoding → K-Means
                                                   │
                     cosine similarity + weighted compatibility → ranking/explanations
```

## ML methodology

1. Load all current student profiles from SQLite.
2. Impute missing numerical and categorical values, scale numerical columns and one-hot encode categorical study attributes with a fitted `ColumnTransformer`.
3. Fit K-Means with `random_state=42`, `n_init=10`, and up to four clusters. Cluster membership is a small study-behaviour signal; it never excludes a candidate.
4. Calculate cosine similarity of transformed feature vectors and use it as part of academic profile fit.
5. Detect directional subject tutoring opportunities: a score below 60 paired with a partner score at or above 75. Reciprocal complementary relationships score highest. Identical strengths alone do not receive complementarity credit.
6. Calculate availability overlap, compatible learning styles, behaviour similarity and goal fit from the two current profiles.
7. Rank by a bounded (0–100) weighted score: academic 30%, complementary skills 30%, availability 15%, learning style 10%, behaviour 5%, goal 10%.
8. Generate human-readable reasons from the same student data and return the top five.

The ML insights page labels the weights as compatibility-score contribution, not learned model feature importance.

## Dataset

`backend/app/seed.py` reproducibly generates the 50-person simulated cohort (one demo profile and 49 generated student profiles) using a fixed random seed and designed subject-strength patterns. Data is seeded at backend startup when the students table is empty, or manually with `python -m app.seed` from `backend/`. The generated records are saved in local SQLite. `data/students.csv` labels the sample as simulated; the database is the runtime source of truth.

## Installation

Requirements: Python 3.10+ and Node.js 18+.

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`; interactive OpenAPI docs are at `http://localhost:8000/docs`. Startup initializes SQLite and seeds simulated records if the database is empty.

### Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL, normally `http://localhost:5173`. The frontend uses `http://localhost:8000/api` by default. Set `VITE_API_URL` to override the API base.

For local security configuration, set `STUDYSYNC_SECRET` before starting the backend. The default secret is only appropriate for a local prototype. Optional `STUDYSYNC_DATABASE_URL` can point SQLAlchemy at a different database URL.

## Demo flow

1. Open the frontend and choose **Explore the demo**, or log in with the demo credentials above.
2. Review academic strengths and preferences at **My profile**; save any edits.
3. Choose **Find a match** and run the live matching pipeline.
4. Open **Why this match?** for data-derived reasons and feedback controls; choose **Compare profiles** for score-by-score detail.
5. Change study time, days or goals in the profile, save and run matching again. Scores and ranks are recomputed from the updated profile.
6. Review **ML insights**, then run **Run ML pipeline** on the demo admin page.

## API endpoints

- `POST /api/auth/register`, `POST /api/auth/login`, `POST /api/auth/demo-login`, `POST /api/auth/logout`
- `GET /api/students/me`, `PUT /api/students/me`, `GET /api/students/{student_id}`
- `GET /api/matching/recommendations/{student_id}`, `GET /api/matching/{student_id}/{partner_id}`
- `POST /api/feedback`
- `GET /api/dashboard`
- `GET /api/ml/clusters`, `GET /api/ml/insights`, `POST /api/ml/run`
- `GET /api/health`

Except registration/login/demo login and health, endpoints require `Authorization: Bearer <access_token>`.

## Testing

From `backend/`, run:

```bash
pytest
```

Tests cover complementary scoring, compatibility bounds and dynamic values, recommendation order, API login, profile privacy, recommendation generation and registration validation.

## Screenshots

_Add screenshots of the landing page, recommendation results, match comparison and ML insights here._

## Future improvements

- Evaluate ranking quality using explicit, longitudinal feedback and offline ranking metrics.
- Add privacy controls, account recovery, refreshable sessions and production-grade secret management.
- Use consent-based real cohorts and an opt-in scheduling/invitation flow.
- Add model monitoring and fairness checks before deployment.
