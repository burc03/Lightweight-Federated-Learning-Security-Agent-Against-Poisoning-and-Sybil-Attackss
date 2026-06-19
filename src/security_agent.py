import numpy as np


def cosine_similarity(a, b):
    """
    Computes cosine similarity between two vectors.
    """
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def detect_suspicious_clients(updates, client_ids, norm_threshold=2.5, similarity_threshold=0.995):
    """
    Detects suspicious clients using two lightweight checks:
    1. Norm-based anomaly detection.
    2. Similarity-based Sybil detection.
    """
    suspicious_clients = set()
    if len(updates) == 0:
        return []

    update_norms = np.array([np.linalg.norm(update) for update in updates])
    median_norm = np.median(update_norms)
    mad = np.median(np.abs(update_norms - median_norm)) + 1e-8

    for i, norm_value in enumerate(update_norms):
        robust_z_score = abs(norm_value - median_norm) / mad
        if robust_z_score > norm_threshold:
            suspicious_clients.add(client_ids[i])

    for i in range(len(updates)):
        for j in range(i + 1, len(updates)):
            sim = cosine_similarity(updates[i], updates[j])
            if sim > similarity_threshold:
                suspicious_clients.add(client_ids[i])
                suspicious_clients.add(client_ids[j])

    return sorted(list(suspicious_clients))
