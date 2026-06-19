import os
import csv


def compute_overheads(results):
    """
    Computes overhead and accuracy recovery metrics.

    Assumes results order:
    1. Normal FL
    2. Under Attack
    3. Under Attack + Agent
    """
    if len(results) < 3:
        return results

    baseline = results[0]
    under_attack = results[1]
    under_attack_agent = results[2]

    baseline_accuracy = baseline["accuracy"]
    attack_accuracy = under_attack["accuracy"]
    agent_accuracy = under_attack_agent["accuracy"]
    attack_time = under_attack["training_time_sec"]
    agent_time = under_attack_agent["training_time_sec"]
    baseline_cpu = baseline["avg_cpu_percent"]
    agent_cpu = under_attack_agent["avg_cpu_percent"]
    baseline_ram = baseline["peak_ram_mb"]
    agent_ram = under_attack_agent["peak_ram_mb"]

    accuracy_drop_from_baseline = round(baseline_accuracy - attack_accuracy, 4)
    accuracy_recovery_from_attack = round(agent_accuracy - attack_accuracy, 4)
    time_overhead_percent = round(((agent_time - attack_time) / attack_time) * 100, 4) if attack_time > 0 else 0.0
    cpu_overhead_percent = round(agent_cpu - baseline_cpu, 4)
    ram_overhead_mb = round(agent_ram - baseline_ram, 4)
    ram_overhead_percent = round(((agent_ram - baseline_ram) / baseline_ram) * 100, 4) if baseline_ram > 0 else 0.0

    for row in results:
        row["accuracy_drop_from_baseline"] = 0.0
        row["accuracy_recovery_from_attack"] = 0.0
        row["time_overhead_percent"] = 0.0
        row["cpu_overhead_percent"] = 0.0
        row["ram_overhead_mb"] = 0.0
        row["ram_overhead_percent"] = 0.0

    under_attack["accuracy_drop_from_baseline"] = accuracy_drop_from_baseline
    under_attack_agent["accuracy_recovery_from_attack"] = accuracy_recovery_from_attack
    under_attack_agent["time_overhead_percent"] = time_overhead_percent
    under_attack_agent["cpu_overhead_percent"] = cpu_overhead_percent
    under_attack_agent["ram_overhead_mb"] = ram_overhead_mb
    under_attack_agent["ram_overhead_percent"] = ram_overhead_percent

    return results


def save_results(results, output_dir="results"):
    """
    Saves experiment results as CSV.
    """
    os.makedirs(output_dir, exist_ok=True)

    if not results:
        return

    attack_type = results[0].get("attack_type", "experiment")
    output_path = os.path.join(output_dir, f"{attack_type}_results.csv")
    fieldnames = list(results[0].keys())

    with open(output_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"[RESULTS] CSV saved to: {output_path}")
