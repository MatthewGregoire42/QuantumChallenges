import math
from qiskit import IBMQ, QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer, compile
from qiskit.providers.ibmq import least_busy

Q = 1   # number of qubits
C = 1   # number of classical bits

# Max sum value for addition
RANGE_MAX = 100
RANGE_MIN = 0

RANGE = abs(RANGE_MAX - RANGE_MIN)

# Number of times to run the circuit
SHOTS = 8192

IBMQ.load_accounts(hub=None)

def measureComputational():
    out = QuantumCircuit(Q,C)
    out.measure([a for a in range(Q)], [b for b in range(C)])
    return out

def measureHadamard():
    out = QuantumCircuit(Q,C)
    for i in range(Q):
        out.h(i)
    return out + measureComputational()

# Maps the interval [0, RANGE] to [-1, 1], and returns
# the corresponding angle on the upper half of the unit circle.
def angle(n):
    return ((n-RANGE_MIN)/RANGE)*math.pi

# Stores the value n in qubit s of the circuit.
def store(n, s):
    out = QuantumCircuit(Q, C)
    out.reset(out.qregs[0][0])
    out.u3(angle(n), 0, 0, s)
    return out

# Increments qubit s by value n
def increment(n, s):
    out = QuantumCircuit(Q, C)
    out.u3(angle(n), 0, 0, s)
    return out

# Returns a quantum circuit that will add a and b and put the result in qubit 0,
# and has a maximum sum of RANGE.
def add(a, b):
    out = QuantumCircuit(Q, C)
    out.reset(out.qregs[0][0])  
    out.u3(angle(a), 0, 0, 0)
    out.u3(angle(b), 0, 0, 0)
    return out

# Turns a quantum job's counts into a number.
def analyze(counts):
    total = 0
    for c in counts:
        total += counts[c]
    
    if '1' in counts:
        percent = counts['1']/total
        # Map the percent onto the unit circle and return the angle,
        # interpreted as an integer between 0 and RANGE.
        distance = -2*percent + 1
        theta = math.acos(distance)
        return math.floor(theta*RANGE/math.pi) + RANGE_MIN
    else:
        return 0


qc = QuantumCircuit(Q,C)

qc += add(14, 28)
qc += measureComputational()

# Run the job on a simulator
backend = Aer.get_backend('qasm_simulator')
sim_job = execute(qc, backend, shots=SHOTS)
counts = sim_job.result().get_counts(qc)
print(counts)
print(analyze(counts))

# Run the job on a physical backend
backend = least_busy(IBMQ.backends())
print(backend.name())
job = execute(qc, backend, shots=SHOTS)
real_counts = job.result().get_counts(qc)
print("Actual result:", real_counts)
print(analyze(real_counts))