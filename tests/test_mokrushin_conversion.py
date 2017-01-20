import unittest
from nfa_converter.automaton import *
from nfa_converter.readwrite import *


class ConversionTest(unittest.TestCase):
    def test_automaton(self):
        enfa = Automaton("eNFA")

        enfa.add_state("q0")
        enfa.add_state("q1")
        enfa.add_state("q2")
        enfa.add_state("q3")
        enfa.add_state("q4")
        enfa.add_state("q5")
        enfa.add_state("q6")

        enfa.set_start_states({"q0", "q3"})
        enfa.set_final_states({"q5", "q6"})
        enfa.set_alphabet({"a", "b"})

        enfa.add_transition("q0", "q1", "ε")
        enfa.add_transition("q0", "q2", "ε")
        enfa.add_transition("q0", "q5", "ε")
        enfa.add_transition("q1", "q6", "b")
        enfa.add_transition("q2", "q2", "a")
        enfa.add_transition("q2", "q2", "b")
        enfa.add_transition("q2", "q5", "b")
        enfa.add_transition("q2", "q6", "b")
        enfa.add_transition("q3", "q2", "ε")
        enfa.add_transition("q3", "q4", "ε")
        enfa.add_transition("q4", "q6", "b")
        enfa.add_transition("q5", "q5", "b")
        enfa.add_transition("q6", "q6", "a")
        enfa.add_transition("q6", "q6", "b")

        print(write(enfa))
        dfa = nfa_to_dfa(enfa)
        print(write(dfa))
