import sys
from qiskit import QuantumCircuit

# Ensure stdout supports UTF-8 for Qiskit circuit drawing on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main():
    # Create a 2-qubit quantum circuit
    qc = QuantumCircuit(2)

    # Apply a Hadamard gate to qubit 0
    qc.h(0)

    # Apply a CNOT gate from qubit 0 to qubit 1
    qc.cx(0, 1)

    # Print the circuit
    print(qc)


if __name__ == "__main__":
    main()

