import unittest
from nfa_converter.readwrite import *


class ReadWriteTest(unittest.TestCase):
    def test_read_valid_first(self):
        try:
            with open("dot_files/sample_valid_first.dot", "r") as dot_file:
                automaton = read(dot_file.read())
        except:
            self.fail()

    def test_read_valid_second(self):
        try:
            with open("dot_files/sample_valid_second.dot", "r") as dot_file:
                automaton = read(dot_file.read())
        except:
            self.fail()

    def test_read_invalid(self):
        try:
            with open("dot_files/sample_invalid.dot", "r") as dot_file:
                automaton = read(dot_file.read())
        except Exception as e:
            print(e)
        else:
            self.fail()
