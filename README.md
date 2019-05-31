# QuantumChallenges
My solutions to a series of challenges designed to engage with quantum computing, using Qiskit. These challenges are from Loren Sklar in the official Qiskit slack.

In addition, `boilerplate.py` has the setup code needed to run quantum experiments (both on local simulators and exterior backends), visualize circuits, retrieve previously run jobs, and visualize the experiment results. Feel free to use it in your own projects!

## Challenge 1 (coinFlip)
"Implement a quantum coin flip. A quantum coin flip returns a single bit with value '0' 50% of the time and '1' 50% of the time."

Just something to get warmed up. This challenge demonstrates the most important aspects of interfacing with Qiskit, without doing anything incredibly complicated. It also makes use of superposition, which is interesting. The plot was made using the `plot_histogram ` function, running the simulation 1024 times.

## Challenge 2 (quantumDice)
"Implement a set of quantum dice. Roll(dice) returns 1 through 8 with equal probability.In addition to standard dice, use entanglement to implement a set of dice with memory. An even roll always follows an odd roll follows an even roll, etc."

This was a fun one. I decided to implement two functions. The first, `roll(n)`, simply rolls a 2^n sided die, using n qubits. The second, `roll_entangled(n, qubits)` was a lot more interesting. It implements the second part of the challenge, but rolls a n general dice, each with 2^qubits sides. Generalizing this was a fun challenge. I also included the output of one run of this program, which successfully rolled 7 entangled 4-sided dice on an actual quantum computer.

## Challenge 3 (montyHall)
Implement the [Monty Hall](https://en.wikipedia.org/wiki/Monty_Hall_problem) problem, both as a classical system and quantum system. Show that by switching doors in the classical case, the odds of winning increase to 67%, but in the quantum case they don't increase above 50%.

This was an interesting challenge, most importantly because Monty can't know what's behind the doors! Therefore it's possible he could open the winning door before the player has a chance to. In my implementation, I simply ignored all the cases when this happened. Perhaps if, in these cases, the prize went to the player, then the overall chance of winning would actually be (50% + 33%) = 83%. Sample output is included as well.
