import numpy as np
from sklearn.cluster import KMeans
from .preprocessing import transform_students

class StudentClusterer:
    def __init__(self):
        self.model = None
        self.transformer = None
        self.student_ids = []
        self.labels = {}
        self.matrix = None

    def fit(self, students):
        frame, matrix, transformer = transform_students(students)
        self.student_ids = [s.student_id if not isinstance(s, dict) else s["student_id"] for s in students]
        if len(self.student_ids) == 0:
            self.model, self.transformer, self.matrix, self.labels = None, None, None, {}
            return self
        self.transformer, self.matrix = transformer, matrix
        count = min(4, len(self.student_ids))
        self.model = KMeans(n_clusters=count, random_state=42, n_init=10)
        values = self.model.fit_predict(matrix) if len(self.student_ids) > 1 else np.array([0])
        self.labels = dict(zip(self.student_ids, values.astype(int).tolist()))
        return self

    def cluster_for(self, student_id):
        return self.labels.get(student_id)

clusterer = StudentClusterer()
