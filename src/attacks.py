import numpy as np


def select_malicious_clients(num_clients, malicious_ratio=0.2, random_seed=42):
    """
    Selects a fixed subset of malicious clients.
    """
    rng = np.random.default_rng(random_seed)
    malicious_count = max(1, int(num_clients * malicious_ratio))
    malicious_clients = set(rng.choice(num_clients, size=malicious_count, replace=False).tolist())

    print("[ATTACK SETUP] Malicious client selection completed.")
    print(f"[ATTACK SETUP] Number of malicious clients: {malicious_count}")
    print(f"[ATTACK SETUP] Malicious clients: {sorted(list(malicious_clients))}")

    return malicious_clients


def apply_model_poisoning(update, scale_factor=-6.0):
    """
    Model poisoning attack.

    A malicious client sends a reversed and amplified model update
    to damage the global model direction.
    """
    poisoned_update = update * scale_factor
    return poisoned_update


def apply_sybil_behavior(update_dict, malicious_clients, noise_scale=0.001):
    """
    Sybil attack simulation.

    Malicious clients send highly similar coordinated model updates.
    This simulates multiple fake identities controlled by the same attacker.
    """
    malicious_clients = sorted(list(malicious_clients))

    if len(malicious_clients) == 0:
        return update_dict

    reference_client = malicious_clients[0]
    if reference_client not in update_dict:
        return update_dict

    reference_update = update_dict[reference_client].copy()
    rng = np.random.default_rng(42)

    for client_id in malicious_clients:
        if client_id in update_dict:
            small_noise = rng.normal(loc=0.0, scale=noise_scale, size=reference_update.shape)
            update_dict[client_id] = reference_update + small_noise

    return update_dict
