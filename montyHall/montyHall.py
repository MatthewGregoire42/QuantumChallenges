from qiskit import QuantumCircuit, BasicAer, IBMQ, execute
from qiskit.providers.ibmq import least_busy
import random
from math import sqrt, floor

# Global backend for the quantum algorithm in this file.
BACKEND = BasicAer.get_backend('qasm_simulator')

# A vector describing the three-state superposition desired
SUPERPOSITION = [0, 1/sqrt(3), 1/sqrt(3), 0, 1/sqrt(3), 0, 0, 0]

DIGITS = 3
SHOTS = 2048

doors = set([0,1,2])

def monty_classical(iterations):

    wins_stay = 0
    wins_switch = 0

    for i in range(iterations):
        playerDoor = random.sample(doors, 1)[0]
        winningDoor = random.sample(doors, 1)[0]

        if playerDoor == winningDoor:
            wins_stay += 1

    for i in range(iterations):
        playerDoor = random.sample(doors, 1)[0]
        winningDoor = random.sample(doors, 1)[0]

        montyDoor = random.sample(doors - set([playerDoor, winningDoor]), 1)[0]
        playerDoor = random.sample(doors - set([playerDoor, montyDoor]), 1)[0]
    
        if playerDoor == winningDoor:
            wins_switch += 1
    
    return round(wins_stay / iterations, DIGITS), round(wins_switch / iterations, DIGITS)

def monty_quantum(iterations):
    
    # The player door is arbitrary, so just always set it to 0.
    # Therefore the win condition is the result state '001'.

    # If the player decides to stay
    qc = QuantumCircuit(3,3)
    qc.initialize(SUPERPOSITION, [0,1,2])
    qc.measure([0,1,2], [0,1,2])

    result_stay = execute(qc, BACKEND, shots=iterations).result().get_counts(qc)
    
    win_ratio_stay = round(result_stay['001'] / (result_stay['001'] + result_stay['010'] + result_stay['100']), DIGITS)

    # If the player decides to switch
    qc = QuantumCircuit(3,3)
    qc.initialize(SUPERPOSITION, [0,1,2])

    # Monty's door is arbitrary, so just always set it to 1
    qc.measure(1, 1)
    qc.measure(0, 0)

    result_switch = execute(qc, BACKEND, shots=iterations).result().get_counts(qc)
    
    # Ignore the cases in which Monty accidentally opened the winning door.
    # (In that case, the car might go to the contestant?)
    acceptable_trials = result_switch['000'] + result_switch['001']

    win_ratio_switch = round(result_switch['001'] / acceptable_trials, DIGITS)

    return win_ratio_stay, win_ratio_switch


classical_stay, classical_switch = monty_classical(SHOTS)
quantum_stay, quantum_switch = monty_quantum(SHOTS)
print("Classical result:")
print("Stay:\t" + str(classical_stay) + "\tSwitch:\t" + str(classical_switch))
print("Simulated quantum result:")
print("Stay:\t" + str(quantum_stay) + "\tSwitch:\t" + str(quantum_switch))

print("Running on an actual quantum computer.")

IBMQ.load_accounts(hub=None)
BACKEND = least_busy(IBMQ.backends(simulator=False))
print("Backend:", BACKEND)

quantum_stay_actual, quantum_switch_actual = monty_quantum(SHOTS)
print("Experimental quantum result:")
print("Stay:\t" + str(quantum_stay_actual) + "\tSwitch:\t" + str(quantum_switch_actual))