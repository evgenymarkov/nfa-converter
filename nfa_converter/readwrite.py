import pydot
from pydot import Graph
from nfa_converter.automaton import Automaton


def read(dot_str) -> Automaton:
    """
    Создание автомата из строки написанной в dot формате.
    """
    # dot формат поддерживает запись нескольких графов в одном файле
    # в данном случае разрешено задавать только один
    read_automatons = pydot.graph_from_dot_data(dot_str)
    if len(read_automatons) != 1:
        raise InvalidAutomatonError("Строка содержит 0 или 2 и более графов.")
    read_automaton: Graph = read_automatons[0]
    if read_automaton.get_type() != "digraph":
        raise InvalidAutomatonError("Автомат не может быть неориентированным.")

    automaton = Automaton(read_automaton.get_name())

    final_states = set()
    for node in read_automaton.get_nodes():
        node_name = _unquote(node.get_name())

        if node_name == "":
            continue

        # Необходимо указывать shape чтобы обозначить обычное это состояние или конечное
        automaton.add_state(node_name)
        if "shape" not in node.get_attributes():
            raise InvalidAutomatonError("Отсутствует атрибут shape у состояния.")

        shape_attr = _unquote(node.get_attributes()["shape"])
        if shape_attr == "doublecircle":
            final_states.add(node_name)
        elif shape_attr != "circle":
            raise InvalidAutomatonError("Недопустимый атрибут shape у состояния.")
    automaton.set_final_states(final_states)

    # Алфавит - множество из всех неповторяющихся символов перехода
    # Символ ε в алфавит не входит
    alphabet = set()
    start_state_set = False
    for edge in read_automaton.get_edges():
        source = _unquote(edge.get_source())
        destination = _unquote(edge.get_destination())

        if source == "":
            if start_state_set:
                raise InvalidAutomatonError("Указано более одного начального состояния.")
            automaton.set_start_state(destination)
            start_state_set = True
            continue

        if "label" not in edge.get_attributes():
            raise InvalidMoveSymbolError("Не указан символ перехода.")

        transition_symbol: str = _unquote(edge.get_attributes()["label"])
        if transition_symbol == "" or len(transition_symbol) > 1:
            raise InvalidMoveSymbolError("Символ перехода задан некорректно.")
        if transition_symbol != "ε":
            alphabet.add(transition_symbol)
        automaton.add_transition(source, destination, transition_symbol)
    automaton.set_alphabet(alphabet)

    if not start_state_set:
        raise InvalidAutomatonError("Не указано начальное состояние.")
    if len(final_states) == 0:
        raise InvalidAutomatonError("Должно быть хотя бы одно конечное состояние.")

    return automaton


def write(automaton: Automaton) -> str:
    """
    Возвращает строку в формате dot описывающую заданный автомат.
    """
    dot_graph = pydot.Dot()
    dot_graph.set_type("digraph")
    dot_graph.set_name(automaton.get_name())

    # Добавление источника из которого идёт стрелка в начальное состояние
    dot_node = pydot.Node(_quote(""), **{"shape": "none"})
    dot_graph.add_node(dot_node)

    for state in automaton.get_states():
        state_attrs = {}
        if state in automaton.get_final_states():
            # Конечные состояния помещаются в двойной круг
            state_attrs["shape"] = "doublecircle"
        else:
            state_attrs["shape"] = "circle"
        dot_node = pydot.Node(_quote(state), **state_attrs)
        dot_graph.add_node(dot_node)

    # Стрелка в начальное состояние
    dot_edge = pydot.Edge(_quote(""), _quote(automaton.get_start_state()))
    dot_graph.add_edge(dot_edge)

    for src, transitions in automaton.get_all_transitions().items():
        for symbol, dst_states in transitions.items():
            for dst in dst_states:
                dot_edge = pydot.Edge(_quote(src), _quote(dst), **{"label": _quote(symbol)})
                dot_graph.add_edge(dot_edge)

    return dot_graph.to_string()


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


def _unquote(string: str) -> str:
    """
    Удаляет двойные кавычки если они строка заключена в них.
    :param string: строка с кавычками или без.
    :return: строку без кавычек по краям, иначе оригинал строки.
    """
    if string.startswith("\"") and string.endswith("\""):
        return string[1:-1]
    else:
        return string


def _quote(string: str) -> str:
    """
    Добавляет двойные кавычки если строка не заключена в них.
    :param string: строка с кавычками или без.
    :return: строку в кавычках если она не была заключена в них, иначе оригинал.
    """
    if not string.startswith("\"") and not string.endswith("\""):
        return f"\"{string}\""
    else:
        return string
