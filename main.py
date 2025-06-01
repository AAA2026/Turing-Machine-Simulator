#!/usr/bin/env python3

"""
TURING MACHINE SIMULATOR

Simutates the operation of a deterministic Turing machine.
"""

# Type definitions:
Symbol = str
State = str
Direction = bool
# State → Symbol → Symbol × State × Direction
TransitionFunction = dict[State, dict[Symbol, tuple[Symbol, State, Direction]]]
Result = bool

# Constant definitions:
RIGHT = False
LEFT = True
BLANK = ""
ACCEPT = True
REJECT = False


class TuringMachine:
    """
    Class to model the behaviour of a Turing machine.
    """

    # Fields marked private by prefixing `_`
    _tape: list[Symbol]  # Memory
    _tape_length: int  # Current size of the tape
    _states: set[State]  # Set of possible states
    _accepting: set[State]  # Set of accepting states, must ⊂ `_states`
    _current_state: State  # Current state, must ∈ `_states`
    _index: int  # Current place in `_tape`
    _delta: TransitionFunction

    def __init__(
        self,
        states: set[State],
        initial_state: State,
        delta: TransitionFunction,
        accepting_states: set[State],
    ):
        if initial_state not in states:
            raise ValueError(f"Initial state '{initial_state}' is not in the set of states")
        
        
        if not accepting_states.issubset(states):
            invalid_states = accepting_states - states
            raise ValueError(f"Accepting states contain invalid states: {invalid_states}")

        self._states = states
        self._current_state = initial_state
        self._delta = delta
        self._accepting = accepting_states

    def input_tape(self, tape: list[Symbol] | str):
        # If tape is empty fill it with a single BLANK
        tape = tape if tape else [BLANK]
        self._tape = list(tape)
        self._tape_length = len(tape)
        self._index = 0

    def go_right(self):
        """
        Pushes the read/write head backward by one cell, expanding the input
        tape if it reaches the start to simulate an infinite tape.
        """
        if self._index == self._tape_length - 1:
            self._tape += [BLANK]
            self._tape_length += 1
        self._index += 1

    def go_left(self):
        """
        Pushes the read/write head forward by one cell, expanding the input tape
        if it reaches the end to simulate an infinite tape.
        """
        if self._index == 0:
            self._tape = [BLANK] + self._tape
            self._tape_length += 1
        else:
            self._index -= 1

    def read(self) -> Symbol:
        return self._tape[self._index]

    def write(self, symbol: Symbol):
        self._tape[self._index] = symbol

    def next(self) -> Result | None:
        
        symbol = self.read()
        state = self._current_state
        if state in self._delta and symbol in self._delta[state]:
            new_symbol, new_state, direction = self._delta[state][symbol]
            self.write(new_symbol)
            self._current_state = new_state
            if direction == RIGHT:
                self.go_right()
            else:
                self.go_left()
            if new_state in self._accepting:
                return ACCEPT
            return None
        else:
            # No valid transition
            return REJECT


def main():
    import json
    import sys
    import time
    import os
    print("TURING MACHINE SIMULATOR\n")
    spec_file = os.path.join(os.path.dirname(__file__), "turing_machine.json")
    try:
        with open(spec_file, 'r', encoding='utf-8') as f:
            spec = json.load(f)
    except Exception as e:
        print(f"Failed to read specification: {e}")
        sys.exit(1)

    # Parse the specification
    try:
        states = set(spec['states'])
        initial_state = spec['initial_state']
        accepting_states = set(spec['accepting_states'])
        delta = {}
        for state, transitions in spec['delta'].items():
            delta[state] = {}
            for symbol, (new_symbol, new_state, direction) in transitions.items():
                delta[state][symbol] = (new_symbol, new_state, direction == 'L')
    except Exception as e:
        print(f"Invalid specification format: {e}")
        sys.exit(1)

    tm = TuringMachine(states, initial_state, delta, accepting_states)

    tape_input = input("Enter the input tape (as a string): ")
    tm.input_tape(list(tape_input))

    max_steps = max(10000, len(tape_input) ** 3)
    steps = 0
    print("\nInitial tape:")
    while True:
        # Print tape and head position
        tape_str = ''.join(tm._tape)
        head_pos = tm._index
        state = tm._current_state
        tape_visual = (
            tape_str[:head_pos] + '[' + (tm._tape[head_pos] if head_pos < len(tm._tape) else BLANK) + ']' + tape_str[head_pos+1:]
        )
        print(f"State: {state} | Tape: {tape_visual}")
        result = tm.next()
        steps += 1
        if result == ACCEPT:
            print("\nInput accepted!")
            break
        elif result == REJECT:
            print("\nInput rejected.")
            break
        if steps > max_steps:
            print("\nComputation exceeded step limit. Possible infinite loop detected.")
            break
        time.sleep(0.2)  # Slow down for visualization


if __name__ == "__main__":
    main()
