import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

NUMERIC = ["python_score", "mathematics_score", "dbms_score", "ai_score", "study_hours", "year"]
CATEGORICAL = ["study_frequency", "learning_pace", "learning_style", "communication_style", "preferred_study_time", "study_goal"]

def student_frame(students):
    rows = []
    for s in students:
        row = s if isinstance(s, dict) else {key: getattr(s, key) for key in NUMERIC + CATEGORICAL}
        rows.append({key: row.get(key) for key in NUMERIC + CATEGORICAL})
    return pd.DataFrame(rows, columns=NUMERIC + CATEGORICAL)

def make_preprocessor():
    numeric = Pipeline([("imputer", SimpleImputer(strategy="median")), ("scale", StandardScaler())])
    categorical = Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("encode", OneHotEncoder(handle_unknown="ignore", sparse_output=False))])
    return ColumnTransformer([("numeric", numeric, NUMERIC), ("categorical", categorical, CATEGORICAL)], verbose_feature_names_out=False)

def transform_students(students):
    frame = student_frame(students)
    if frame.empty:
        return frame, None, None
    transformer = make_preprocessor()
    matrix = transformer.fit_transform(frame)
    return frame, matrix, transformer
