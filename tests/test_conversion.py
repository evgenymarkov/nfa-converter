import unittest
from nfa_converter.automaton import *
from nfa_converter.readwrite import *


class ConversionTest(unittest.TestCase):
    def test_automaton_first(self):
        enfa = Automaton("eNFA")

        for i in range(11):
            enfa.add_state(str(i))

        enfa.set_start_state("0")
        enfa.set_final_states({"10"})
        enfa.set_alphabet({"a", "b"})

        enfa.add_transition("0", "1", "ε")
        enfa.add_transition("0", "7", "ε")
        enfa.add_transition("1", "2", "ε")
        enfa.add_transition("1", "4", "ε")
        enfa.add_transition("2", "3", "a")
        enfa.add_transition("4", "5", "b")
        enfa.add_transition("3", "6", "ε")
        enfa.add_transition("5", "6", "ε")
        enfa.add_transition("6", "1", "ε")
        enfa.add_transition("6", "7", "ε")
        enfa.add_transition("7", "8", "a")
        enfa.add_transition("8", "9", "b")
        enfa.add_transition("9", "10", "b")

        print(write(enfa))
        dfa = nfa_to_dfa(enfa)
        print(write(dfa))
