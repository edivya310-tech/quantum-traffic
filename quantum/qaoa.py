"""Quantum Approximate Optimization Algorithm (QAOA) for Urban Traffic Optimization.

MATHEMATICAL AND QUANTUM FOUNDATIONS:
1. Qubit Mapping:
   - 4 binary variables (x1, x2, x3, x4) map to 4 qubits (qubits 0, 1, 2, 3).
   - Qubit 0 -> J1 (x1)
   - Qubit 1 -> J2 (x2)
   - Qubit 2 -> J3 (x3)
   - Qubit 3 -> J4 (x4)

2. Binary to Spin Transformation (x_i -> Z_i):
   - Binary decision x_i in {0, 1} is mapped to Pauli-Z operator Z_i:
     x_i = (I - Z_i) / 2
   - State |0> (eigenvalue +1 of Z) maps to x_i = 0 (East-West priority).
   - State |1> (eigenvalue -1 of Z) maps to x_i = 1 (North-South priority).

3. Cost Hamiltonian H_C Derivation:
   - Classical QUBO: C(x) = sum_i (Q_ii * x_i) + offset
   - Substituting x_i = (I - Z_i) / 2:
     H_C = sum_i Q_ii * (I - Z_i) / 2 = sum_i (Q_ii / 2) * I - sum_i (Q_ii / 2) * Z_i
   - Omitting identity terms (constant energy offset causes only a global phase shift):
     H_C = - sum_i (Q_ii / 2) Z_i
   - Cost Unitary U(H_C, gamma) = exp(-i * gamma * H_C) = prod_i exp(i * gamma * (Q_ii / 2) * Z_i)
   - In Qiskit, RZ(theta) = exp(-i * (theta / 2) * Z).
   - Equating: -theta_i / 2 = gamma * Q_ii / 2  =>  theta_i = -gamma * Q_ii
   - Therefore, U(H_C, gamma) is implemented by RZ(-gamma * Q_ii) on qubit i.

4. Mixer Hamiltonian H_M and Unitary U(H_M, beta):
   - Standard transverse field X mixer: H_M = sum_i X_i
   - Mixer Unitary U(H_M, beta) = exp(-i * beta * H_M) = prod_i exp(-i * beta * X_i)
   - In Qiskit, RX(theta) = exp(-i * (theta / 2) * X).
   - Equating: theta / 2 = beta  =>  theta = 2 * beta
   - Implemented by RX(2 * beta) on each qubit i.

5. Hybrid Quantum-Classical Framework:
   - QAOA prepares a parameterized quantum state |psi(gamma, beta)> = U(H_M, beta) U(H_C, gamma) |+>^4.
   - A classical optimizer searches for parameters (gamma, beta) minimizing expected QUBO energy.
   - The final quantum state measurement is probabilistic, yielding bitstrings according to |<x|psi>|^2.
"""

import itertools
from typing import Any, Dict, List, Tuple
import numpy as np

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

try:
    from quantum.qubo import build_qubo, evaluate_qubo
    from quantum.traffic_model import TrafficIntersection
except ModuleNotFoundError:
    from qubo import build_qubo, evaluate_qubo
    from traffic_model import TrafficIntersection


def qiskit_bitstring_to_config(bitstring: str) -> List[int]:
    """Convert Qiskit measurement string (little-endian: q3q2q1q0) to project order [x1, x2, x3, x4].

    In Qiskit, the bitstring returned by get_counts() displays higher-indexed qubits on the left.
    Example: bitstring "1010" -> q3=1, q2=0, q1=1, q0=0.
    Reversing gives: q0=0 (x1), q1=1 (x2), q2=0 (x3), q3=1 (x4) -> [0, 1, 0, 1].

    Args:
        bitstring: 4-character string of '0's and '1's from Qiskit measurement.

    Returns:
        List[int] representing [x1, x2, x3, x4].
    """
    return [int(b) for b in reversed(bitstring)]


def create_qaoa_circuit(
    Q: np.ndarray, gamma: float, beta: float, p: int = 1
) -> QuantumCircuit:
    """Build a QAOA QuantumCircuit for a given QUBO matrix Q and parameters (gamma, beta).

    Args:
        Q: 4x4 diagonal numpy array representing QUBO coefficients Q_ii.
        gamma: Cost Hamiltonian rotation parameter.
        beta: Mixer Hamiltonian rotation parameter.
        p: QAOA circuit depth / number of layers (default 1).

    Returns:
        Qiskit QuantumCircuit with 4 qubits and 4 classical measurement bits.
    """
    n_qubits = Q.shape[0]
    qc = QuantumCircuit(n_qubits, n_qubits)

    # 1. Initial State: Equal superposition |+>^4 via Hadamard gates
    for i in range(n_qubits):
        qc.h(i)

    # 2. QAOA Layers (p layers)
    for _ in range(p):
        # A. Cost Unitary U(H_C, gamma)
        for i in range(n_qubits):
            q_ii = Q[i, i]
            theta = -gamma * q_ii
            qc.rz(theta, i)

        # B. Mixer Unitary U(H_M, beta)
        for i in range(n_qubits):
            qc.rx(2.0 * beta, i)

    # 3. Measurement
    qc.measure(range(n_qubits), range(n_qubits))

    return qc


def optimize_qaoa_parameters(
    Q: np.ndarray,
    offset: float,
    p: int = 1,
    grid_steps: int = 16,
    shots: int = 512,
    seed: int = 42,
) -> Tuple[float, float]:
    """Perform classical grid search to find optimal (gamma, beta) minimizing expected energy.

    Args:
        Q: 4x4 QUBO matrix.
        offset: QUBO offset float.
        p: QAOA depth.
        grid_steps: Number of evaluation points per parameter dimension.
        shots: Number of simulator shots per grid point.
        seed: Random seed for simulator reproducibility.

    Returns:
        Tuple[float, float]: (best_gamma, best_beta)
    """
    simulator = AerSimulator()

    gammas = np.linspace(0.0, np.pi, grid_steps)
    betas = np.linspace(0.0, np.pi / 2.0, grid_steps)

    best_gamma = 0.0
    best_beta = 0.0
    min_expected_cost = float("inf")

    for gamma in gammas:
        for beta in betas:
            qc = create_qaoa_circuit(Q, gamma, beta, p=p)
            result = simulator.run(qc, shots=shots, seed_simulator=seed).result()
            counts = result.get_counts()

            # Calculate expected (average) cost over all shots
            total_shots = sum(counts.values())
            expected_cost = 0.0

            for bitstring, count in counts.items():
                config = qiskit_bitstring_to_config(bitstring)
                cost = evaluate_qubo(Q, config, offset)
                expected_cost += (count / total_shots) * cost

            if expected_cost < min_expected_cost:
                min_expected_cost = expected_cost
                best_gamma = float(gamma)
                best_beta = float(beta)

    return best_gamma, best_beta


def run_qaoa(
    intersections: List[TrafficIntersection],
    p: int = 1,
    shots: int = 1024,
    seed: int = 42,
) -> Dict[str, Any]:
    """Execute full QAOA traffic optimization pipeline.

    Args:
        intersections: List of 4 TrafficIntersection objects.
        p: QAOA circuit depth.
        shots: Number of measurement shots.
        seed: Random seed for reproducible simulation.

    Returns:
        Dict containing QAOA execution results:
        - "method": "QAOA"
        - "configuration": List[int] best measured configuration
        - "cost": float best measured QUBO cost
        - "gamma": float optimal gamma parameter
        - "beta": float optimal beta parameter
        - "counts": Dict[str, int] raw measurement counts
        - "shots": int total shots
        - "circuit": QuantumCircuit final executed QAOA circuit
        - "expected_cost": float average energy across all shots
    """
    Q, offset = build_qubo(intersections)

    # 1. Classical parameter search for optimal (gamma, beta)
    best_gamma, best_beta = optimize_qaoa_parameters(
        Q, offset, p=p, grid_steps=16, shots=512, seed=seed
    )

    # 2. Build final QAOA circuit with optimal parameters
    final_qc = create_qaoa_circuit(Q, best_gamma, best_beta, p=p)

    # 3. Simulate final circuit with requested shots
    simulator = AerSimulator()
    result = simulator.run(final_qc, shots=shots, seed_simulator=seed).result()
    counts = result.get_counts()

    # 4. Analyze measurement counts and find best measured configuration
    best_measured_config: List[int] = []
    best_measured_cost = float("inf")
    total_shots = sum(counts.values())
    expected_cost = 0.0

    for bitstring, count in counts.items():
        config = qiskit_bitstring_to_config(bitstring)
        cost = evaluate_qubo(Q, config, offset)
        expected_cost += (count / total_shots) * cost

        if cost < best_measured_cost:
            best_measured_cost = cost
            best_measured_config = config

    return {
        "method": "QAOA",
        "configuration": best_measured_config,
        "cost": best_measured_cost,
        "gamma": best_gamma,
        "beta": best_beta,
        "counts": counts,
        "shots": shots,
        "circuit": final_qc,
        "expected_cost": expected_cost,
    }
