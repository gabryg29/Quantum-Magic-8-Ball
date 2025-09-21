from __future__ import annotations
from qiskit import QuantumCircuit
from qiskit.primitives import Sampler
from typing import List

# Magic 8 Ball responses (8 = 2^3)
RESPONSES: List[str] = [
    "Yes",
    "No",
    "Maybe",
    "Definitely",
    "Ask again later",
    "Certainly not",
    "Absolutely",
    "Doubtful",
]

def build_circuit() -> QuantumCircuit:
    """3-qubit superposition; measure all."""
    qc = QuantumCircuit(3, 3)
    qc.h([0, 1, 2])
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc

def quantum_pick(shots: int = 1) -> int:
    """Run the circuit with a local Sampler and return an integer 0–7."""
    qc = build_circuit()
    sampler = Sampler()
    result = sampler.run([qc], shots=shots).result()
    counts = result[0].data.meas.get_counts()  # e.g., {"000": 1}
    # Take the most frequent outcome (with shots=1 it’s just the only one)
    bitstring = max(counts, key=counts.get)
    # Qiskit returns classical bits little-endian by default; reverse to human-read
    idx = int(bitstring[::-1], 2)
    return idx

def quantum_magic_8_ball() -> str:
    idx = quantum_pick(shots=1)
    return RESPONSES[idx]

if __name__ == "__main__":
    print("🎱 Quantum Magic 8 Ball says:", quantum_magic_8_ball())

    # --- Optional: IBM Quantum Runtime (uncomment and configure) ---
    # from qiskit_ibm_runtime import QiskitRuntimeService, Session, SamplerV2
    # service = QiskitRuntimeService(channel="ibm_quantum", instance="ibm-q/open/main")
    # with Session(service=service, backend="ibm_brisbane") as session:
    #     runtime_sampler = SamplerV2(session=session)
    #     qc = build_circuit()
    #     job = runtime_sampler.run([qc], shots=1)
    #     counts = job.result()[0].data.meas.get_counts()
    #     bitstring = max(counts, key=counts.get)
    #     idx = int(bitstring[::-1], 2)
    #     print("🎱 (Runtime) Quantum Magic 8 Ball says:", RESPONSES[idx])
