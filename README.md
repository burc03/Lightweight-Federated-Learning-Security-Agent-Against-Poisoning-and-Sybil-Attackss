# Lightweight Federated Learning Security Agent Against Poisoning and Sybil Attacks

This project implements a lightweight security agent for a simulated Federated Learning environment.

## Project Goal

The goal is to detect suspicious client updates before aggregation and protect the global model against:

1. Model Poisoning Attack
2. Sybil Attack

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Model Poisoning Attack experiment:

```bash
python main.py --attack poisoning
```

Run Sybil Attack experiment:

```bash
python main.py --attack sybil
```

## Experiment Scenarios

Each attack is tested with three scenarios:

1. Normal FL  
   No attack and no security agent.

2. Under Attack  
   Attack is enabled but the security agent is disabled.

3. Under Attack + Agent  
   Attack is enabled and the security agent is enabled.

## Metrics

The project reports:

- Accuracy
- Training time
- Average CPU usage
- Peak RAM usage
- Detection rate
- False positive rate
- Filtered clients
- Accuracy drop from baseline
- Accuracy recovery from attack
- Time overhead
- CPU overhead
- RAM overhead

## Main Files

- `main.py`: Runs experiments.
- `src/data_utils.py`: Generates and splits dataset.
- `src/federated_learning.py`: Implements FL training.
- `src/attacks.py`: Implements poisoning and Sybil attacks.
- `src/security_agent.py`: Detects suspicious clients.
- `src/metrics.py`: Computes evaluation metrics.
- `src/visualization.py`: Generates plots.
