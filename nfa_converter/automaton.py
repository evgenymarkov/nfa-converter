import os
from enum import Enum
from typing import Set, Dict


class AutomatonType(Enum):
    DFA = 1  # детерминированный конечный автомат
    NFA = 2  # недетерминированный конечный автомат
    eNFA = 3  # недетерминированный конечный автомат с ε-переходами


class StateAlreadyExists(Exception):
    """
    Ошибка возникающая при повторном добавлении в автомат одинаковых состояний.
    """
    pass


class StateNotFoundError(Exception):
    """
    Ошибка возникающая при обращении к несуществующему состоянию.
    """
    pass


class Automaton:
    def __init__(self, name: str):
        """
        Инициализация автомата.
        :param name: название автомата.
        """
        self._name = name
        self._states = set()
        self._start_state = None
        self._final_states = set()
        self._transitions = dict()
        self._alphabet = set()

    def get_name(self) -> str:
        """
        Получение названия автомата.
        :return: название автомата.
        """
        return self._name

    def get_states(self) -> Set[str]:
        """
        Получение множества состояний.
        :return: множество строк-идентификаторов состояний.
        """
        return self._states

    def get_start_state(self) -> str:
        """
        Получение стартовой вершины.
        :return: строка-идентификатор стартовой вершины.
        """
        return self._start_state

    def get_final_states(self) -> Set[str]:
        """
        Получение множества конечных состояний.
        :return: множество строк-идентификаторов конечных состояний.
        """
        return self._final_states

    def get_alphabet(self) -> Set[str]:
        """
        Получение алфавита используемого в автомате,
        :return: множество символов алфавита.
        """
        return self._alphabet

    def get_all_transitions(self) -> Dict[str, Dict[str, Set[str]]]:
        """
        Получение всех переходов автомата.
        :return: словарь переходов из всех состояний.
        """
        return self._transitions

    def get_transitions_from(self, state: str) -> Dict[str, Set[str]]:
        """
        Получение переходов из указанного состояния.
        :param state: строка-идентификатор состояния.
        :return: словарь пар вида "символ: множество_состояний"
        """
        if state not in self._states:
            raise StateNotFoundError(f"{state} отсутствует в списке состояний.")
        return self._transitions[state]

    def get_type(self) -> AutomatonType:
        """
        Получение типа автомата.
        :return: если автомат содержит ε-переходы, то возвращается тип eNFA,
        если ε-переходов нет, но по одному символу можноп перейти в несколько состояний, то NFA,
        иначе DFA.
        """
        is_nfa = False
        for src, transitions in self.get_all_transitions().items():
            if "ε" in transitions:
                return AutomatonType.eNFA
            for symbol, dst_states in transitions.items():
                if len(dst_states) >= 2:
                    is_nfa = True
        return AutomatonType.NFA if is_nfa else AutomatonType.DFA

    def add_state(self, state: str):
        """
        Добавление состояния.
        :param state: строка-идентификатор состояния.
        """
        if state in self._states:
            raise StateAlreadyExists
        self._states.add(state)

    def add_transition(self, from_state: str, to_state: str, symbol: str):
        """
        Добавление перехода.
        :param from_state: состояние из которого осуществляется переход.
        :param to_state: состояние в которое осуществляется переход.
        :param symbol: символ по которому осуществляется переход.
        """
        if from_state not in self._states:
            raise StateNotFoundError(f"{from_state} отсутствует в списке состояний.")
        if to_state not in self._states:
            raise StateNotFoundError(f"{to_state} отсутствует в списке состояний.")

        if from_state not in self._transitions:
            self._transitions[from_state] = {}
        if symbol not in self._transitions[from_state]:
            self._transitions[from_state][symbol] = set()
        self._transitions[from_state][symbol].add(to_state)

    def set_start_state(self, state: str):
        """
        Указание стартового состояния.
        :param state: строка-идентификатор стартового состояния.
        """
        if state not in self._states:
            raise StateNotFoundError(f"\"{state}\" нет в списке состояний.")
        self._start_state = state

    def set_final_states(self, states: set):
        """
        Указание множества конечных состояний.
        :param states: множество строк-идентификаторов конечных состояний.
        """
        for state in states:
            if state not in self._states:
                raise StateNotFoundError(f"\"{state}\" нет в списке состояний.")
        self._final_states = states

    def set_alphabet(self, alphabet: set):
        """
        Указание используемого в автомате алфавита.
        :param alphabet: множество символов алфавита.
        """
        self._alphabet = alphabet

    def __repr__(self) -> str:
        """
        Получение строкового представления автомата.
        """
        return f"Automaton {self._name}{os.linesep}" + \
               f"States: {self._states}{os.linesep}" + \
               f"Start state: {self._start_state}{os.linesep}" + \
               f"Final states: {self._final_states}{os.linesep}" + \
               f"Alphabet: {self._alphabet}{os.linesep}" + \
               f"Transitions: {self._transitions}"


def nfa_to_dfa(nfa: Automaton) -> Automaton:
    pass
