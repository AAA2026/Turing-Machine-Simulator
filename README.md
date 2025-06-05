## Turing Machine Simulator

This project provides a Python-based simulator for a deterministic Turing machine. It allows users to define a Turing machine's behavior through a JSON specification file and observe its step-by-step execution on a given input tape. The simulator is designed for educational purposes, offering a clear visualization of the machine's state transitions and tape manipulations.

### Features

The simulator implements a classic Turing machine model with a single, potentially infinite tape. The tape is simulated dynamically, expanding to the left or right as needed when the read/write head reaches the current boundaries. The machine's configuration, including its states, alphabet (implicitly defined by symbols in the transitions), initial state, accepting states, and transition function, is loaded from an external JSON file. During execution, the simulator prints the current state of the machine and the contents of the tape, highlighting the position of the read/write head for easy tracking. To prevent potential infinite loops, a maximum step count is enforced, halting the simulation if it exceeds this limit.

### JSON Specification Format

The behavior of the Turing machine is defined in a JSON file, typically named `turing_machine.json`, located in the same directory as the main script. This file must adhere to the following structure:

*   `states`: An array of strings, listing all possible states the machine can be in.
*   `initial_state`: A string specifying the state the machine starts in. This state must be present in the `states` array.
*   `accepting_states`: An array of strings, listing the states that signify acceptance of the input tape. All states listed here must also be present in the `states` array.
*   `delta`: An object representing the transition function. The keys of this object are the current states (must be in `states`). The value for each state key is another object where keys are the symbols read from the tape in that state. The value for each symbol key is an array containing three elements: the symbol to write back to the tape, the next state to transition into, and the direction to move the tape head ('R' for right, 'L' for left).

The provided `turing_machine.json` serves as an example, defining a machine that recognizes the language {0^n 1^n | n >= 1}.

### Setup

To use the simulator, you need Python 3 installed on your system. No external libraries beyond the standard Python library are required. Ensure that the `main.py` script and the `turing_machine.json` specification file are placed in the same directory.

### Usage

Navigate to the project directory in your terminal and run the script using the command:

```bash
python3 main.py
```

The script will first load the machine specification from `turing_machine.json`. If the file is missing or incorrectly formatted, an error message will be displayed. Upon successful loading, the simulator will prompt you to enter the initial input tape as a string. After you provide the input, the simulation begins. The program will print the initial tape configuration and then proceed step-by-step, showing the current state and the tape contents with the head position marked (e.g., `[symbol]`) at each transition. A small delay is introduced between steps for better visualization. The simulation concludes when the machine enters an accepting state (outputting "Input accepted!"), enters a state with no valid transition for the current symbol (outputting "Input rejected."), or exceeds the maximum step limit (outputting a warning about a potential infinite loop).

### Example Execution 

```
Enter the input tape (as a string): 0011

Initial tape:
State: zero | Tape: [0]011
State: one | Tape: X[0]11
State: one | Tape: X0[1]1
State: x | Tape: X0[Y]1
State: x | Tape: X[0]Y1
State: zero | Tape: X[X]Y1
State: one | Tape: XX[Y]1
State: one | Tape: XXY[1]
State: x | Tape: XX[Y]Y
State: x | Tape: X[X]YY
State: zero | Tape: XX[Y]Y
State: blank | Tape: XXY[Y]
State: blank | Tape: XXYY[]
State: accept | Tape: XXY[Y]

Input accepted!
```

This README provides a comprehensive guide to understanding, setting up, and using the Turing Machine Simulator.
