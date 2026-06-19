import numpy as np


def generate_dataset(n_samples=30000, n_features=20, random_seed=42):
    """
    Generates a synthetic binary classification dataset.
    """
    rng = np.random.default_rng(random_seed)
    X = rng.normal(0, 1, size=(n_samples, n_features))
    true_weights = rng.normal(0, 1, size=n_features)
    logits = X @ true_weights
    probabilities = 1 / (1 + np.exp(-np.clip(logits, -500, 500)))
    y = (probabilities >= 0.5).astype(int)

    indices = rng.permutation(n_samples)
    X = X[indices]
    y = y[indices]
    split_index = int(n_samples * 0.8)

    X_train = X[:split_index]
    y_train = y[:split_index]
    X_test = X[split_index:]
    y_test = y[split_index:]

    return X_train, y_train, X_test, y_test


def split_clients(X_train, y_train, num_clients=20, random_seed=42):
    """
    Splits training data among clients for local federated learning simulation.
    """
    rng = np.random.default_rng(random_seed)
    indices = rng.permutation(len(X_train))
    client_indices = np.array_split(indices, num_clients)

    client_data = []
    for client_id, idx in enumerate(client_indices):
        client_data.append({"client_id": client_id, "X": X_train[idx], "y": y_train[idx]})

    return client_data
