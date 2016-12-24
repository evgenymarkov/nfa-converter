import pydot
from pydot import Graph, Node
from nfa_converter.automaton import Automaton


def read(dot_str) -> Automaton:
    """
    Создание автомата из строки написанной в dot формате.
    """
    read_automatons = pydot.graph_from_dot_data(dot_str)
    if len(read_automatons) != 1:
        raise InvalidAutomatonError("Строка содержит 0 или 1 и более графов.")
    read_automaton: Graph = read_automatons[0]

    if read_automaton.get_type() != "digraph":
        raise InvalidAutomatonError("Автомат не может быть неориентированным.")

    automaton = Automaton(read_automaton.get_name())

    final_states = set()
    for node in read_automaton.get_nodes():
        node_name = unquote(node.get_name())

        if node_name == "":
            continue

        automaton.add_state(node_name)
        if "shape" not in node.get_attributes():
            raise InvalidAutomatonError("Отсутствует атрибут shape у состояния.")

        shape_attr = unquote(node.get_attributes()["shape"])
        if shape_attr == "doublecircle":
            final_states.add(node_name)
    automaton.set_final_states(final_states)

    alphabet = set()
    empty_state_set = False
    for edge in read_automaton.get_edges():
        source = unquote(edge.get_source())
        destination = unquote(edge.get_destination())

        if source == "":
            if empty_state_set:
                raise InvalidAutomatonError("Указано более одного начального состояния.")
            automaton.set_start_state(destination)
            empty_state_set = True
            continue

        if "label" not in edge.get_attributes():
            raise InvalidMoveSymbolError("Не указан символ перехода.")

        transition_symbol: str = unquote(edge.get_attributes()["label"])
        if transition_symbol == "" or len(transition_symbol) > 1:
            raise InvalidMoveSymbolError("Символ перехода задан некорректно.")
        if transition_symbol != "ε":
            alphabet.add(transition_symbol)

        automaton.add_transition(source,
                                 destination,
                                 transition_symbol)
    automaton.set_alphabet(alphabet)

    return automaton


def write(automaton: Automaton) -> str:
    """
    Возвращает строку в формате dot описывающую заданный автомат.
    """
    pass


class InvalidAutomatonError(Exception):
    """
    Ошибка говорящая о том, что автомат задан неправильно.
    """
    pass


class InvalidMoveSymbolError(Exception):
    """
    Отсутсвует символ перехода или указан некорректный.
    """
    pass


def unquote(string: str) -> str:
    if string.startswith("\"") and string.endswith("\""):
        return string[1:-1]
    else:
        return string
