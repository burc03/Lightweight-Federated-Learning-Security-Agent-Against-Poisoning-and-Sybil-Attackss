# Lightweight Federated Learning Security Agent Against Poisoning and Sybil Attacks

This project implements a lightweight security agent for a simulated Federated Learning environment. The main purpose of the system is to detect suspicious client updates before aggregation and protect the global model against malicious client behavior.

The project focuses on two different attack types:

* Model Poisoning Attack
* Sybil Attack

Both attacks can be executed separately from the terminal, and each attack is evaluated with and without the proposed security agent.

---

## Project Overview

Federated Learning is a distributed machine learning approach where multiple clients train a shared model without sending their raw data to a central server. Each client trains the model locally and sends only its model update to the server. The server then aggregates these updates to improve the global model.

Although this approach provides a privacy advantage, it is still vulnerable to malicious clients. A malicious client may send a harmful update to damage the global model, or multiple malicious clients may behave in a coordinated way to influence the aggregation process.

To address this problem, this project adds a lightweight security agent before the aggregation step. The agent analyzes client updates, detects suspicious clients, and filters risky updates before Federated Averaging.

---

## Main Features

* Local Federated Learning simulation
* Separate Model Poisoning Attack experiment
* Separate Sybil Attack experiment
* Lightweight security agent
* Norm-based anomaly detection
* Cosine similarity-based Sybil detection
* Accuracy and training time measurement
* CPU and RAM overhead measurement
* Detection rate and false positive rate calculation
* CSV result output generation
* Accuracy and training time plot generation

---

## Attack Types

### 1. Model Poisoning Attack

In the Model Poisoning Attack scenario, malicious clients send reversed and amplified model updates. These updates are designed to damage the global model direction and reduce model accuracy.

Run the poisoning attack experiment with:

```bash
python main.py --attack poisoning
```

### 2. Sybil Attack

In the Sybil Attack scenario, malicious clients send highly similar coordinated updates. This simulates fake or coordinated client identities trying to influence the aggregation process.

Run the Sybil attack experiment with:

```bash
python main.py --attack sybil
```

---

## Experiment Scenarios

Each attack is evaluated with three scenarios:

### 1. Normal FL

No attack and no security agent are enabled.
This scenario is used as the baseline.

### 2. Under Attack

The selected attack is enabled, but the security agent is disabled.
This scenario shows how the attack affects the global model.

### 3. Under Attack + Agent

The selected attack and the security agent are both enabled.
This scenario shows whether the agent can detect suspicious clients and recover model performance.

---

## How to Run

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

### 2. Run Model Poisoning Attack

```bash
python main.py --attack poisoning
```

### 3. Run Sybil Attack

```bash
python main.py --attack sybil
```

---

## Example Terminal Summary

At the end of each experiment, the program prints a professional summary that answers the following questions:

1. How long does the model train and what is the accuracy without the security agent?
2. What is the model accuracy under attack without the security agent?
3. How much does the model recover under attack with the agent, and what CPU/RAM overhead does the agent introduce?

Example output structure:

```text
PROFESSIONAL EXPERIMENT SUMMARY - POISONING ATTACK

QUESTION 1:
Normal FL accuracy = ...
training time = ...

QUESTION 2:
Under poisoning attack without security agent accuracy = ...

QUESTION 3:
Under poisoning attack with security agent accuracy = ...
Accuracy recovery from attack = ...
CPU overhead = ...
RAM overhead = ...
```

---

## Metrics

The project reports the following metrics:

* Accuracy
* Training time
* Average CPU usage
* Peak RAM usage
* Detection rate
* False positive rate
* Filtered clients
* Accuracy drop from baseline
* Accuracy recovery from attack
* Time overhead
* CPU overhead
* RAM overhead

---

## Project Structure

```text
.
├── main.py
├── README.md
├── requirements.txt
└── src
    ├── __init__.py
    ├── attacks.py
    ├── data_utils.py
    ├── federated_learning.py
    ├── metrics.py
    ├── security_agent.py
    └── visualization.py
```

---

## File Descriptions

### `main.py`

Runs the full experiment. It takes the attack type as a terminal argument and executes three scenarios for each attack.

### `src/data_utils.py`

Generates the synthetic binary classification dataset and splits the training data among clients.

### `src/federated_learning.py`

Implements local training, Federated Averaging, attack execution, security agent execution, and model evaluation.

### `src/attacks.py`

Implements malicious client selection, Model Poisoning Attack, and Sybil Attack behavior.

### `src/security_agent.py`

Detects suspicious clients using update norm analysis and cosine similarity.

### `src/metrics.py`

Computes accuracy drop, accuracy recovery, time overhead, CPU overhead, and RAM overhead.

### `src/visualization.py`

Generates result plots for accuracy and training time.

---

## Implementation Details

The system uses a synthetic binary classification dataset and a logistic regression model. The simulation contains 20 clients, and 20% of them are selected as malicious clients when an attack is enabled.

The security agent uses two lightweight detection methods:

1. **Norm-based anomaly detection**
   Detects updates with abnormal magnitude.

2. **Cosine similarity-based detection**
   Detects highly similar coordinated updates, especially for Sybil-like behavior.

Suspicious updates are removed before aggregation. Only trusted client updates are used to update the global model.

---

## Notes

This project is implemented locally in Python.

It does not use:

* LLM APIs
* Paid AI services
* Cloud-based AI tools

The goal is to provide a simple, understandable, and measurable security defense for Federated Learning.
