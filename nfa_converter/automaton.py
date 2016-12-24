import os


class Automaton:
    def __init__(self, name: str):
        self._name = name
        self._states = set()
        self._start_state = None
        self._final_states = set()
        self._transitions = dict()
        self._alphabet = set()

    def get_states(self) -> set:
        return self._states

    def get_start_state(self) -> int:
        return self._start_state

    def get_final_states(self) -> set:
        return self._final_states

    def get_alphabet(self) -> set:
        return self._alphabet

    def get_transitions(self, state: int, symbol: str):
        pass

    def add_state(self, state):
        if state in self._states:
            raise StateAlreadyExists
        self._states.add(state)

    def add_transition(self, from_state, to_state, symbol):
        if not isinstance(symbol, str):
            raise InvalidSymbolTypeError()
        if from_state not in self._states:
            self._states.add(from_state)
        if to_state not in self._states:
            self._states.add(to_state)

        if from_state not in self._transitions:
            self._transitions[from_state] = {}
        self._transitions[from_state][symbol] = to_state

    def set_start_state(self, state):
        if state not in self._states:
            raise StateNotFoundError(f"\"{state}\" нет в списке состояний.")
        self._start_state = state

    def set_final_states(self, states: set):
        for state in states:
            if state not in self._states:
                raise StateNotFoundError(f"\"{state}\" нет в списке состояний.")
        self._final_states = states

    def set_alphabet(self, alphabet: set):
        self._alphabet = alphabet

    def __repr__(self):
        return f"Automaton {self._name}{os.linesep}" + \
               f"States: {self._states}{os.linesep}" + \
               f"Start state: {self._start_state}{os.linesep}" + \
               f"Final states: {self._final_states}{os.linesep}" + \
               f"Alphabet: {self._alphabet}{os.linesep}" + \
               f"Transitions: {self._transitions}"


def nfa_to_dfa(nfa: Automaton) -> Automaton:
    pass


class StateAlreadyExists(Exception):
    pass


class StateNotFoundError(Exception):
    pass


class InvalidSymbolTypeError(Exception):
    pass
