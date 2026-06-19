import os
import matplotlib.pyplot as plt


def create_plots(results, output_dir="results"):
    """
    Creates simple result plots for accuracy and training time.
    """
    os.makedirs(output_dir, exist_ok=True)

    if not results:
        return

    attack_type = results[0].get("attack_type", "experiment")
    scenarios = [row["scenario"] for row in results]
    accuracies = [row["accuracy"] for row in results]
    training_times = [row["training_time_sec"] for row in results]

    plt.figure(figsize=(10, 5))
    plt.bar(scenarios, accuracies)
    plt.ylabel("Accuracy")
    plt.title(f"Accuracy Comparison - {attack_type.capitalize()} Attack")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    accuracy_path = os.path.join(output_dir, f"{attack_type}_accuracy.png")
    plt.savefig(accuracy_path)
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.bar(scenarios, training_times)
    plt.ylabel("Training Time (sec)")
    plt.title(f"Training Time Comparison - {attack_type.capitalize()} Attack")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    time_path = os.path.join(output_dir, f"{attack_type}_training_time.png")
    plt.savefig(time_path)
    plt.close()

    print(f"[PLOTS] Accuracy plot saved to: {accuracy_path}")
    print(f"[PLOTS] Training time plot saved to: {time_path}")
