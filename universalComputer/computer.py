import math
from qiskit import IBMQ, QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer, compile
from qiskit.providers.ibmq import least_busy

Q = 8   # number of qubits
C = 8   # number of classical bits

IBMQ.load_accounts(hub=None)

qc = QuantumCircuit(Q,C)

# Returns a quantum circuit that puts a AND b in qubit s
def andQ(a, b, s):
    out = QuantumCircuit(Q,C)
    out.reset(out.qregs[0][s])
    out.ccx(a, b, s)
    return out

# Returns a quantum circuit that puts a OR b in qubit s
def orQ(a, b, s):
    out = QuantumCircuit(Q, C)
    out.x(a)
    out.x(b)
    out.reset(out.qregs[0][s])
    out.x(s)
    out.ccx(a, b, s)
    out.x(a)
    out.x(b)
    return out

# Returns a quantum circuit that puts a XOR b in qubit s
def xorQ(a, b, s):
    out = QuantumCircuit(Q, C)
    out.reset(out.qregs[0][s])
    out.cx(a, b)
    out.cx(b, s)
    out.cx(a, b)
    return out

# A half adder circuit with inputs a and b, and outputs
# s (a + b) and cout
def halfAdder(a, b, s, co):
    out = QuantumCircuit(Q, C)
    out += andQ(a, b, co)
    out += xorQ(a, b, s)
    return out

# Returns a quantum circuit that puts ci + a + b in qubit s, with co in qubit co
# ci: carry in, s: sum, co: carry out
# e1, e2, and e3 are ancilla qubits
def add(ci, a, b, s, co, e1, e2, e3):
    out = QuantumCircuit(Q, C)
    out += halfAdder(a, b, e1, e3)
    out += halfAdder(ci, e1, s, e2)
    out += orQ(e2, e3, co)
    return out

def measureComputational():
    out = QuantumCircuit(Q,C)
    out.measure([a for a in range(Q)], [b for b in range(C)])
    return out

def measureHadamard():
    out = QuantumCircuit(Q,C)
    for i in range(Q):
        out.h(i)
    return out + measureComputational()

# Test each possible combination of carry-in, a, and b inputs
qc.h(7)
qc.h(6)
qc.h(5)
qc += add(7, 6, 5, 4, 3, 2, 1, 0)
qc.measure([7, 6, 5, 4, 3], [7, 6, 5, 4, 3])

# Number of times to run the circuit
SHOTS = 1024

# Run the job on a simulator
backend = Aer.get_backend('qasm_simulator')
sim_job = execute(qc, backend, shots=SHOTS)
counts = sim_job.result().get_counts(qc)
print(counts)

# # Run the job on a physical backend
# backend = IBMQ.get_backend('ibmq_16_melbourne')
# job = execute(qc, backend, shots=SHOTS)
# counts = job.result().get_counts(qc)
# print("Actual result:", real_counts)

m = 0
m_str = ''
for c in counts:
    ci = c[0]
    a = c[1]
    b = c[2]
    s = c[3]
    co = c[4]
    print(ci, "+", a, "+", b, "=", s, "with carry", co, "\t", counts[c])
    if counts[c] > m:
        m = counts[c]
        m_str = c

# print("")
# print("Final result:")
# print(m_str[0], "+", m_str[1], "+", m_str[2], "=", m_str[3], "with carry", m_str[4], "\t", m)