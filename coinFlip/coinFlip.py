from qiskit import QuantumCircuit, BasicAer, IBMQ, execute
from qiskit.visualization import plot_histogram

Q = 1   # number of qubits
C = 1   # number of classical bits

backend = BasicAer.get_backend('qasm_simulator')

def flip():
    qc = QuantumCircuit(Q,C)

    # Quantum circuit goes here
    qc.h(0)
    qc.measure(0, 0)

    counts = execute(qc, backend, shots=1).result().get_counts(qc)
    
    try:
        counts['0']
        return 0
    except:
        return 1

zeros = 0
ones = 0

# Flip the coin 1000 times

for i in range(1000):
    if flip() == 0:
        zeros += 1
    else:
        ones += 1

print("Final result:")
print("0 :", zeros, " 1 :", ones)