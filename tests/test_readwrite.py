import unittest
from nfa_converter.automaton import *
from nfa_converter.readwrite import *


class ReadWriteTest(unittest.TestCase):
    def test_read_valid(self):
        with open("dot_files/sample1.dot", "r") as dot_file:
            automaton = read(dot_file.read())
        print(automaton)

    def test_read_invalid_dfa(self):
        pass
