import os
from enum import Enum
from queue import Queue
from typing import FrozenSet, Set, Dict


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
        self._start_states = set()
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

    def get_start_states(self) -> Set[str]:
        """
        Получение множества стартовых вершин.
        :return: строки-идентификаторы стартовых вершин.
        """
        return self._start_states

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
        if state not in self._transitions:
            return {}
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

    def set_start_states(self, states: set):
        """
        Указание множества начальных состояний.
        :param states: набор идентификаторов стартовых состояний.
        """
        for new_state in states:
            if new_state not in self._states:
                raise StateNotFoundError(f"\"{new_state}\" нет в списке состояний.")
            self._start_states.add(new_state)

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
               f"Start state: {self._start_states}{os.linesep}" + \
               f"Final states: {self._final_states}{os.linesep}" + \
               f"Alphabet: {self._alphabet}{os.linesep}" + \
               f"Transitions: {self._transitions}"


def nfa_to_dfa(nfa: Automaton) -> Automaton:
    """
    Получение по заданному недетерминированному автомату эквивалентного
    детерминированного. Использован алгоритм описанный в следующем документе:
    http://web.cecs.pdx.edu/~harry/compilers/slides/LexicalPart3.pdf
    :param nfa: недетерминированный автомат.
    :return: эквивалентный детерминированный автомат.
    """
    dfa_transitions: Dict[FrozenSet[str], Dict[str, FrozenSet[str]]] = {}
    dfa_states: Dict[FrozenSet[str], str] = {}
    unmarked_states = Queue()

    state_mark = "A"
    eps_closure_start = frozenset(_epsilon_set_closure(nfa, frozenset(nfa.get_start_states())))
    dfa_states[eps_closure_start] = state_mark
    unmarked_states.put(eps_closure_start)

    new_alphabet: Set[str] = set()
    while not unmarked_states.empty():
        current_dfa_state = unmarked_states.get()
        dfa_transitions[current_dfa_state] = {}
        for symbol in nfa.get_alphabet():
            next_dfa_state = _epsilon_set_closure(nfa, _nfa_moves(nfa, current_dfa_state, symbol))
            if len(next_dfa_state) > 0:
                if next_dfa_state not in dfa_states:
                    state_mark = chr(ord(state_mark) + 1)
                    dfa_states[next_dfa_state] = state_mark
                    unmarked_states.put(next_dfa_state)
                dfa_transitions[current_dfa_state][symbol] = next_dfa_state
                new_alphabet.add(symbol)

    dfa = Automaton("DFA")
    final_states = set()
    for dfa_state in dfa_states:
        # Группе состояний из НКА присваивается новый идентификатор и добавляется в ДКА
        dfa.add_state(dfa_states[dfa_state])

        # Если хотя бы одно состояние из НКА было конечным,
        # то новое соответствующее состояние ДКА также будет конечным.
        for nfa_state in dfa_state:
            if nfa_state in nfa.get_final_states():
                final_states.add(dfa_states[dfa_state])
                break

    for dfa_state in dfa_states:
        for symbol, dst in dfa_transitions[dfa_state].items():
            from_state_mark = dfa_states[dfa_state]
            to_state_mark = dfa_states[dst]
            dfa.add_transition(from_state_mark, to_state_mark, symbol)

    dfa.set_start_states({"A"})
    dfa.set_final_states(final_states)
    dfa.set_alphabet(new_alphabet)

    return dfa


def _nfa_moves(nfa: Automaton, from_states: FrozenSet[str], symbol: str) -> FrozenSet[str]:
    """
    Получение набора состояний достижимых из указанного множества по заданному переходу.
    :param nfa: недетерминированный автомат.
    :param from_states: множество состояний из которых будет призведён поиск достижимых.
    :param symbol: символ перехода.
    :return: неизменяемое множество состояний достижимых из указанных по заданному символу.
    """
    moves: Set[str] = set()

    for state in from_states:
        if symbol in nfa.get_transitions_from(state):
            moves.update(nfa.get_transitions_from(state)[symbol])

    return frozenset(moves)


def _epsilon_set_closure(nfa: Automaton, from_states: FrozenSet[str]) -> FrozenSet[str]:
    """
    Получение состояний, которые достижимы по ε-переходам из множества указанных состояний.
    :param nfa: недетерминированный автомат.
    :param from_states: множество состояний из которых будет произведён поиск достижимых.
    :return: неизменяемое множество состояний достижимых из указанных по ε-переходам.
    """
    eps_closure = set()
    for state in from_states:
        eps_closure.update(_epsilon_closure(nfa, state))
    return frozenset(eps_closure)


def _epsilon_closure(nfa: Automaton, state: str) -> Set[str]:
    """
    Получение состояний, которые достижимы по ε-переходам из указанного состояния.
    :param nfa: недетерминированный автомат.
    :param state: состояние из которого будет поиск достижимых состояний.
    :return: множество состояний достижимых по ε-переходам.
    """
    reachable_states: Set[str] = set()
    reachable_states.add(state)

    if "ε" in nfa.get_transitions_from(state):
        for dst in nfa.get_transitions_from(state)["ε"]:
            reachable_states |= _epsilon_closure(nfa, dst)

    return reachable_states
