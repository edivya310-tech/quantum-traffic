"""Test script and validation suite for QAOA Traffic Optimizer."""

import sys
import numpy as np

# Ensure stdout handles UTF-8 encoding on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

try:
    from quantum.traffic_model import create_sample_traffic
    from quantum.classical_optimizer import optimize_traffic
    from quantum.qubo import build_qubo, evaluate_qubo
    from quantum.qaoa import run_qaoa, qiskit_bitstring_to_config
except ModuleNotFoundError:
    from traffic_model import create_sample_traffic
    from classical_optimizer import optimize_traffic
    from qubo import build_qubo, evaluate_qubo
    from qaoa import run_qaoa, qiskit_bitstring_to_config


def main() -> None:
    # 1. Load sample traffic data
    intersections = create_sample_traffic()
    Q, offset = build_qubo(intersections)

    # 2. Run QAOA optimization pipeline
    p = 1
    shots = 1024
    qaoa_result = run_qaoa(intersections, p=p, shots=shots, seed=42)

    # 3. Run Classical optimizer for comparison
    classical_result = optimize_traffic(intersections)

    qaoa_config = qaoa_result["configuration"]
    qaoa_cost = qaoa_result["cost"]
    best_gamma = qaoa_result["gamma"]
    best_beta = qaoa_result["beta"]
    counts = qaoa_result["counts"]

    classical_config = classical_result["best_configuration"]
    classical_cost = classical_result["best_cost"]

    matched = (qaoa_config == classical_config) and np.isclose(
        qaoa_cost, classical_cost
    )
    match_str = "YES" if matched else "NO"

    # 4. Print results formatted as required
    print("=" * 50)
    print("QAOA TRAFFIC OPTIMIZATION")
    print("=" * 50)
    print()
    print(f"Number of qubits: {qaoa_result['circuit'].num_qubits}")
    print(f"QAOA depth p: {p}")
    print(f"Shots: {shots}")
    print()
    print(f"Best gamma: {best_gamma:.4f}")
    print(f"Best beta: {best_beta:.4f}")
    print()
    print("Measurement counts (Qiskit bitstrings q3q2q1q0 -> project config):")
    for bitstring, count in sorted(
        counts.items(), key=lambda x: x[1], reverse=True
    ):
        cfg = qiskit_bitstring_to_config(bitstring)
        qubo_c = evaluate_qubo(Q, cfg, offset)
        print(
            f"  Bitstring '{bitstring}' -> Config {cfg} | Count: {count:4d} | Cost: {qubo_c}"
        )
    print()
    print(f"Best QAOA configuration: {qaoa_config}")
    print(f"Best QAOA cost: {qaoa_cost}")
    print()
    print("Classical optimum:")
    print(f"  Configuration: {classical_config}")
    print(f"  Cost: {classical_cost}")
    print()
    print(f"QAOA matched classical optimum: {match_str}")
    print("=" * 50)
    print()

    # 5. Print final QAOA Circuit diagram
    print("Final QAOA Circuit:")
    print(qaoa_result["circuit"])
    print()

    # ==================================================
    # VALIDATION / ASSERTIONS
    # ==================================================

    print("=" * 50)
    print("VALIDATION")
    print("=" * 50)

    # 1. QAOA uses exactly 4 qubits
    assert (
        qaoa_result["circuit"].num_qubits == 4
    ), f"TEST 1 FAILED: Expected 4 qubits, got {qaoa_result['circuit'].num_qubits}"
    print("QAOA qubit count (4 qubits): PASS")

    # 2. Returned configuration has length 4
    assert (
        len(qaoa_config) == 4
    ), f"TEST 2 FAILED: Configuration length must be 4, got {len(qaoa_config)}"
    print("Returned configuration length (4 bits): PASS")

    # 3. Every configuration bit is 0 or 1
    assert all(
        val in (0, 1) for val in qaoa_config
    ), f"TEST 3 FAILED: Invalid binary values in {qaoa_config}"
    print("Binary configuration values (0 or 1): PASS")

    # 4. QAOA cost is calculated using existing QUBO evaluator
    eval_cost = evaluate_qubo(Q, qaoa_config, offset)
    assert np.isclose(
        qaoa_cost, eval_cost
    ), f"TEST 4 FAILED: QAOA cost {qaoa_cost} != evaluate_qubo cost {eval_cost}"
    print("Cost evaluation using existing QUBO evaluator: PASS")

    # 5. Measurement counts are non-empty
    assert len(counts) > 0, "TEST 5 FAILED: Measurement counts are empty"
    print("Measurement counts non-empty: PASS")

    # 6. Total measurement counts equal requested shots
    total_counts = sum(counts.values())
    assert (
        total_counts == shots
    ), f"TEST 6 FAILED: Total counts {total_counts} != requested shots {shots}"
    print(f"Total measurement counts equal shots ({shots}): PASS")

    # 7. Helper bitstring conversion validation: "1010" -> [0, 1, 0, 1]
    assert qiskit_bitstring_to_config("1010") == [
        0,
        1,
        0,
        1,
    ], "TEST 7 FAILED: Bitstring conversion helper invalid"
    print("Qiskit bitstring conversion helper: PASS")

    print()
    print("All QAOA validation assertions passed successfully.")
    print("=" * 50)


if __name__ == "__main__":
    main()
