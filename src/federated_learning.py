import time
import numpy as np

from src.attacks import select_malicious_clients, apply_model_poisoning, apply_sybil_behavior
from src.security_agent import detect_suspicious_clients


def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))


def initialize_model(n_features, random_seed=42):
    rng = np.random.default_rng(random_seed)
    return rng.normal(0, 0.01, size=n_features)


def local_train(global_model, X, y, local_epochs=2, learning_rate=0.1):
    """
    Performs local logistic regression training and returns the model update.
    """
    local_model = global_model.copy()
    for _ in range(local_epochs):
        predictions = sigmoid(X @ local_model)
        gradient = X.T @ (predictions - y) / len(y)
        local_model -= learning_rate * gradient
    update = local_model - global_model
    return update


def aggregate_updates(global_model, updates):
    """
    Federated averaging over selected client updates.
    """
    if len(updates) == 0:
        return global_model
    mean_update = np.mean(updates, axis=0)
    return global_model + mean_update


def evaluate_model(model, X_test, y_test):
    predictions = sigmoid(X_test @ model)
    predicted_labels = (predictions >= 0.5).astype(int)
    return float(np.mean(predicted_labels == y_test))


def run_federated_training(
    model,
    client_data,
    X_test,
    y_test,
    num_rounds=25,
    local_epochs=2,
    learning_rate=0.15,
    malicious_ratio=0.2,
    attack_enabled=False,
    attack_type="poisoning",
    security_agent_enabled=False,
    random_seed=42,
):
    """
    Runs federated learning and optionally enables one selected attack type and the security agent.
    """
    start_time = time.perf_counter()
    malicious_clients = set()

    if attack_enabled:
        malicious_clients = select_malicious_clients(num_clients=len(client_data), malicious_ratio=malicious_ratio, random_seed=random_seed)
        print("\n[ATTACK SETUP]")
        print(f"Selected attack type: {attack_type}")
        print(f"Total clients: {len(client_data)}")
        print(f"Malicious ratio: {malicious_ratio}")
        print(f"Malicious clients: {sorted(list(malicious_clients))}")

    ram_samples = []
    detection_hits = 0
    false_positives = 0
    total_malicious_checks = 0
    total_benign_checks = 0
    filtered_clients_total = 0

    try:
        import psutil
        process = psutil.Process()
        psutil_available = True
        cpu_start = process.cpu_times()
    except Exception:
        process = None
        psutil_available = False
        cpu_start = None

    for round_id in range(num_rounds):
        updates = []
        client_ids = []

        if attack_enabled and round_id == 0:
            print(f"\n[ROUND {round_id + 1}] Attack execution started.")

        for client in client_data:
            client_id = client["client_id"]
            update = local_train(global_model=model, X=client["X"], y=client["y"], local_epochs=local_epochs, learning_rate=learning_rate)

            if attack_enabled and attack_type == "poisoning" and client_id in malicious_clients:
                if round_id == 0:
                    print(f"[POISONING ATTACK] Client {client_id} sends a reversed and amplified model update.")
                update = apply_model_poisoning(update)

            updates.append(update)
            client_ids.append(client_id)

        if attack_enabled and attack_type == "sybil":
            if round_id == 0:
                print("[SYBIL ATTACK] Malicious clients send highly similar coordinated updates.")
                print(f"[SYBIL ATTACK] Sybil clients: {sorted(list(malicious_clients))}")

            update_dict = {client_ids[i]: updates[i] for i in range(len(client_ids))}
            update_dict = apply_sybil_behavior(update_dict, malicious_clients)
            updates = [update_dict[client_id] for client_id in client_ids]

        trusted_updates = updates

        if security_agent_enabled:
            suspicious_clients = detect_suspicious_clients(updates=updates, client_ids=client_ids)
            suspicious_set = set(suspicious_clients)
            filtered_clients_total += len(suspicious_set)
            detection_hits += len(suspicious_set.intersection(malicious_clients))
            false_positives += len(suspicious_set.difference(malicious_clients))
            total_malicious_checks += len(malicious_clients)
            total_benign_checks += len(client_ids) - len(malicious_clients)

            if attack_enabled and round_id == 0:
                print("\n[SECURITY AGENT]")
                print(f"Suspicious clients detected: {sorted(list(suspicious_set))}")
                print("[SECURITY AGENT] Suspicious updates are filtered before aggregation.")

            trusted_updates = [updates[i] for i, client_id in enumerate(client_ids) if client_id not in suspicious_set]

        model = aggregate_updates(model, trusted_updates)

        if psutil_available:
            ram_samples.append(process.memory_info().rss / (1024 * 1024))

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    avg_cpu_percent = 0.0
    if psutil_available and cpu_start is not None and elapsed_time > 0:
        cpu_end = process.cpu_times()
        cpu_time_used = (cpu_end.user - cpu_start.user) + (cpu_end.system - cpu_start.system)
        avg_cpu_percent = (cpu_time_used / elapsed_time) * 100

    detection_rate = detection_hits / total_malicious_checks if total_malicious_checks > 0 else 0.0
    false_positive_rate = false_positives / total_benign_checks if total_benign_checks > 0 else 0.0

    metrics = {
        "training_time_sec": elapsed_time,
        "avg_cpu_percent": float(avg_cpu_percent),
        "peak_ram_mb": float(np.max(ram_samples)) if ram_samples else 0.0,
        "detection_rate": detection_rate,
        "false_positive_rate": false_positive_rate,
        "filtered_clients_total": filtered_clients_total,
    }
    return model, metrics
