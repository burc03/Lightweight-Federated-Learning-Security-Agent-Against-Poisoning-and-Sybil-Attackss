import argparse

from src.data_utils import generate_dataset, split_clients
from src.federated_learning import initialize_model, run_federated_training, evaluate_model
from src.metrics import compute_overheads, save_results
from src.visualization import create_plots


def print_professional_summary(results, attack_type):
    baseline = results[0]
    under_attack = results[1]
    under_attack_agent = results[2]

    baseline_accuracy = baseline["accuracy"]
    baseline_time = baseline["training_time_sec"]
    attack_accuracy = under_attack["accuracy"]
    attack_time = under_attack["training_time_sec"]
    agent_accuracy = under_attack_agent["accuracy"]
    agent_time = under_attack_agent["training_time_sec"]

    accuracy_drop = round(baseline_accuracy - attack_accuracy, 4)
    accuracy_recovery = round(agent_accuracy - attack_accuracy, 4)
    time_overhead_percent = round(((agent_time - attack_time) / attack_time) * 100, 4) if attack_time > 0 else 0.0

    print("\n" + "=" * 100)
    print(f"PROFESSIONAL EXPERIMENT SUMMARY - {attack_type.upper()} ATTACK")
    print("=" * 100)
    print("\nQUESTION 1:")
    print("Güvenlik ajanı yokken model ne kadar sürede eğitiliyor ve doğruluğu nedir?")
    print(f"Answer: Normal FL accuracy = {baseline_accuracy:.4f}, training time = {baseline_time:.4f} seconds.")
    print("\nQUESTION 2:")
    print("Saldırı altındayken, ajan yokken modelin doğruluğu nedir?")
    print(f"Answer: Under {attack_type} attack without security agent, accuracy = {attack_accuracy:.4f}. Accuracy drop from baseline = {accuracy_drop:.4f}.")
    print("\nQUESTION 3:")
    print("Saldırı altındayken ajan varken model ne kadar toparlanıyor ve ek CPU/RAM maliyeti nedir?")
    print(f"Answer: Under {attack_type} attack with security agent, accuracy = {agent_accuracy:.4f}. Accuracy recovery from attack = {accuracy_recovery:.4f}.")
    print("\nAgent Overhead:")
    print(f"Time overhead = {time_overhead_percent:.4f}%")
    print(f"CPU overhead = {under_attack_agent.get('cpu_overhead_percent', 0.0):.4f}%")
    print(f"RAM overhead = {under_attack_agent.get('ram_overhead_mb', 0.0):.4f} MB")
    print(f"RAM overhead percent = {under_attack_agent.get('ram_overhead_percent', 0.0):.4f}%")
    print("\nDetection Metrics:")
    print(f"Detection rate = {under_attack_agent['detection_rate']:.4f}")
    print(f"False positive rate = {under_attack_agent['false_positive_rate']:.4f}")
    print(f"Filtered clients total = {under_attack_agent['filtered_clients_total']}")
    print("\nScenario Table:")
    for row in results:
        print(row)
    print("=" * 100)


def run_experiment(attack_type):
    print("\n" + "#" * 100)
    print("FEDERATED LEARNING SECURITY AGENT EXPERIMENT")
    print(f"SELECTED ATTACK TYPE: {attack_type.upper()}")
    print("#" * 100)

    X_train, y_train, X_test, y_test = generate_dataset(n_samples=30000, n_features=20, random_seed=42)
    client_data = split_clients(X_train, y_train, num_clients=20, random_seed=42)

    base_config = {"num_rounds": 80, "local_epochs": 4, "learning_rate": 0.15, "malicious_ratio": 0.20, "random_seed": 42}
    scenarios = [
        {"scenario": "Normal FL", "attack_enabled": False, "security_agent_enabled": False},
        {"scenario": f"Under {attack_type.capitalize()} Attack", "attack_enabled": True, "security_agent_enabled": False},
        {"scenario": f"Under {attack_type.capitalize()} Attack + Agent", "attack_enabled": True, "security_agent_enabled": True},
    ]

    results = []
    for scenario in scenarios:
        print("\n" + "-" * 100)
        print(f"Running scenario: {scenario['scenario']}")
        print(f"Attack type: {attack_type}")
        print(f"Attack enabled: {scenario['attack_enabled']}")
        print(f"Security agent enabled: {scenario['security_agent_enabled']}")
        print("-" * 100)

        if not scenario["attack_enabled"]:
            print("[ATTACK] No attack is applied in this scenario.")
        elif attack_type == "poisoning":
            print("[ATTACK] Model Poisoning Attack is active.")
            print("[ATTACK] Malicious clients will send reversed and amplified updates.")
        elif attack_type == "sybil":
            print("[ATTACK] Sybil Attack is active.")
            print("[ATTACK] Malicious clients will send highly similar coordinated updates.")

        if scenario["security_agent_enabled"]:
            print("[DEFENSE] Security Agent is enabled.")
            print("[DEFENSE] Suspicious updates will be detected and filtered before aggregation.")
        else:
            print("[DEFENSE] Security Agent is disabled.")

        model = initialize_model(n_features=X_train.shape[1], random_seed=42)
        trained_model, experiment_metrics = run_federated_training(
            model=model,
            client_data=client_data,
            X_test=X_test,
            y_test=y_test,
            num_rounds=base_config["num_rounds"],
            local_epochs=base_config["local_epochs"],
            learning_rate=base_config["learning_rate"],
            malicious_ratio=base_config["malicious_ratio"],
            attack_enabled=scenario["attack_enabled"],
            attack_type=attack_type,
            security_agent_enabled=scenario["security_agent_enabled"],
            random_seed=base_config["random_seed"],
        )
        final_accuracy = evaluate_model(trained_model, X_test, y_test)
        row = {
            "attack_type": attack_type,
            "scenario": scenario["scenario"],
            "attack": scenario["attack_enabled"],
            "security_agent": scenario["security_agent_enabled"],
            "accuracy": round(final_accuracy, 4),
            "training_time_sec": round(experiment_metrics["training_time_sec"], 4),
            "avg_cpu_percent": round(experiment_metrics["avg_cpu_percent"], 4),
            "peak_ram_mb": round(experiment_metrics["peak_ram_mb"], 4),
            "detection_rate": round(experiment_metrics["detection_rate"], 4),
            "false_positive_rate": round(experiment_metrics["false_positive_rate"], 4),
            "filtered_clients_total": experiment_metrics["filtered_clients_total"],
        }
        print("\n[SCENARIO RESULT]")
        print(row)
        results.append(row)

    results = compute_overheads(results)
    save_results(results, output_dir="results")
    create_plots(results, output_dir="results")
    print_professional_summary(results, attack_type)
    print("\nResults saved in the results/ folder.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Federated Learning Security Agent Attack Experiment")
    parser.add_argument("--attack", choices=["poisoning", "sybil"], required=True, help="Choose attack type: poisoning or sybil")
    args = parser.parse_args()
    run_experiment(args.attack)
