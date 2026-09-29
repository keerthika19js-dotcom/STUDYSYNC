import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def cosine_score(vector_a, vector_b):
    """Return cosine similarity normalized to a stable 0..1 range."""
    raw = float(cosine_similarity(np.asarray(vector_a).reshape(1, -1), np.asarray(vector_b).reshape(1, -1))[0, 0])
    return max(0.0, min(1.0, raw))
