# In general, not all imports are needed. Important ones include:
# IBMQ, QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer

from qiskit import *
from qiskit.visualization import plot_histogram
from qiskit.providers.ibmq import least_busy

Q = 3   # number of qubits
C = 3   # number of classical bits

provider = IBMQ.load_account()

# Quantum circuit goes here. For reference, this creates a three-qubit Bell state.
qc = QuantumCircuit(Q,C)

qc.h(0)
qc.cx(0, 1)
qc.cx(0,2)
qc.measure([0,1,2], [0,1,2])

# Draw the quantum circuit and output it to a file. 
# qc.draw(output='mpl').savefig("C:\\Users\\matth\\Documents\\Documents\\Qiskit\\__circuit_file___.png")

print(qc.draw(output="text"))

SHOTS = 1024

# Run the job on a simulator
backend = Aer.get_backend('qasm_simulator')
sim_job = execute(qc, backend, shots=SHOTS)
counts = sim_job.result().get_counts(qc)
print("Simulator results:", counts)

# Run the job on a real quantum computer
backend = least_busy(provider.backends(simulator=False))
print("The least busy backend is ", backend)
job = execute(qc, backend, shots=SHOTS)
real_counts = job.result().get_counts(qc)
print("Actual result:", real_counts)

# # Retrieve an already existing job on a certain backend
# # Change NAME and JOB_ID to access the correct job
# NAME = 'ibmqx4'
# JOB_ID = ''
# backend = provider.get_backend(NAME)
# backend.retrieve_job(JOB_ID)
# old_counts = job.result().get_counts(qc)
# print("Old result:", old_counts)

# # Plot the results of the computation as a histogram.
# # ***change the file name each time***
# # Still a work in progress to get the formatting correct!

# plot_histogram([counts, real_counts], legend=['Simulated', 'Actual'], title='Experiment', figsize=(9,5)).savefig("C:\\Users\\matth\\Documents\\Documents\\Qiskit\\__result_file__.png")