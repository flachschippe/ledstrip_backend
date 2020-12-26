import unittest
from animations.parameter import ParameterBase


class ParameterBaseTests(unittest.TestCase):

    def parameterbase_returns_same_value(self):
        i = ParameterBase(1)
        self.assertEqual(1, i.get_value())
        s = ParameterBase("s")
        self.assertEqual("s", s.get_value())



