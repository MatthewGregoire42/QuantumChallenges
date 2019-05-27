from qiskit import QuantumCircuit, BasicAer, IBMQ, execute
from qiskit.visualization import plot_histogram
from qiskit.providers.ibmq import least_busy

# Global backend for all quantum algorithms in this file.
BACKEND = BasicAer.get_backend('qasm_simulator')

# May want to increase shots if using a larger number of qubits
SHOTS = 8192

# Rolls one 2**qbits sided die
def roll(qbits):
    qc = QuantumCircuit(qbits,qbits)

    # Quantum circuit goes here
    for i in range(qbits):
        qc.h(i)
        qc.measure(i,i)

    counts = execute(qc, BACKEND, shots=SHOTS).result().get_counts(qc)
    
    c = ''
    max_frequency = 0
    for item in counts:
        if counts[item] > max_frequency:
            max_frequency = counts[item]
            c = item

    return int(c, 2)

# Rolls n entangled dice with a certain number of qubits (default 3),
# such that an odd roll always follows an even roll, and
# an even roll always follows an odd roll.
# The dice will have 2**qbits sides each.
def roll_entangled(n, qbits=3):

    qc = QuantumCircuit(qbits*n, qbits*n)

    # First <#qbits> bits are the first die, second <#qbits> are the second die, etc.

    for x in range(n):
        for i in range(qbits):
            bit = i + qbits*x
            # Completely randomize the first die
            if (x == 0):
                qc.h(bit)
            # Randomize the upper bits of other dice
            elif (i < qbits-1):
                qc.h(bit)
            # Entangle the 1s places of all dice
            elif (i == qbits-1):
                qc.cx(bit-qbits, bit)
                qc.x(bit)

    for i in range(qbits*n):
        qc.measure(i, i)
    
    counts = execute(qc, BACKEND, shots=SHOTS).result().get_counts(qc)

    # Make c the most common element in the results.
    # Also, python and qiskit have opposite bit orders, 
    # so flip the bit order of c.
    c = ''
    max_frequency = 0
    for item in counts:
        if counts[item] > max_frequency:
            max_frequency = counts[item]
            c = item[::-1] 

    dice = []
    for i in range(n):
        dice.append(int(c[qbits*i:(qbits*i)+qbits],2))

    return dice

# Quickly check that a given roll is actually working
def working(dice):
    works = True
    for i in range(len(dice)):
        if i < len(dice)-1:
            if (dice[i] % 2) == (dice[i+1] % 2):
                return not works
    return works

for i in range(20):
    toss = roll_entangled(6,3)
    print(toss, ("Working :)" if working(toss) else "Not working :("))

# Now for an actual test!

IBMQ.load_accounts(hub=None)
BACKEND = least_busy(IBMQ.backends(simulator=False, filters=lambda x: x.configuration().n_qubits >= 14))

print("Rolling dice with an actual quantum computer")
print("Backend:", BACKEND.name())
toss = roll_entangled(7,2)
print(toss, ("Working :)" if working(toss) else "Not working :("))
