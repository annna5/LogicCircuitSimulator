""" Module containing unit tests """
import unittest
import sys
sys.path.append('..')
from LogicCircuitSimulator.main.main import Main
from LogicCircuitSimulator.main.simulator import Simulator
from LogicCircuitSimulator.devices.gates import GateAnd, Switch, GateOr,\
               GateNand, GateNor, GateXor, GateBuffor, GateNot, Bulb, Knot

class TestGates(unittest.TestCase):
    """ class with unittest methods """
    def setUp(self):
        """ set up initializations """
        self.my_main = Main()
        self.sim = Simulator(self.my_main)
        self.sw1 = Switch(self.sim)
        self.sw2 = Switch(self.sim)

    def test_gate_and(self):
        """ tasting gate_and state """
        gate = GateAnd(self.sim)
        gate.inputs = []
        gate.update()
        gate.inputs.append(self.sw1)
        gate.inputs.append(self.sw2)
        self.sw1.state = 0
        self.sw2.state = 0
        gate.update()
        res1 = gate.state
        self.sw2.state = 1
        gate.update()
        res2 = gate.state
        self.sw1.state = 1
        gate.update()
        res3 = gate.state
        self.sw2.state = 0
        gate.update()
        res4 = gate.state
        self.assertEqual([res1, res2, res3, res4], [0, 0, 1, 0])

    def test_gate_or(self):
        """ tasting gate or state """
        gate = GateOr(self.sim)
        gate.inputs = []
        gate.update()
        gate.inputs.append(self.sw1)
        gate.inputs.append(self.sw2)
        self.sw1.state = 0
        self.sw2.state = 0
        gate.update()
        res1 = gate.state
        self.sw2.state = 1
        gate.update()
        res2 = gate.state
        self.sw1.state = 1
        gate.update()
        res3 = gate.state
        self.sw2.state = 0
        gate.update()
        res4 = gate.state
        self.assertEqual([res1, res2, res3, res4], [0, 1, 1, 1])

    def test_gate_nand(self):
        """ tasting gate nand state """
        gate = GateNand(self.sim)
        gate.inputs = []
        gate.update()
        gate.inputs.append(self.sw1)
        gate.inputs.append(self.sw2)
        self.sw1.state = 0
        self.sw2.state = 0
        gate.update()
        res1 = gate.state
        self.sw2.state = 1
        gate.update()
        res2 = gate.state
        self.sw1.state = 1
        gate.update()
        res3 = gate.state
        self.sw2.state = 0
        gate.update()
        res4 = gate.state
        self.assertEqual([res1, res2, res3, res4], [1, 1, 0, 1])

    def test_gate_nor(self):
        """ tasting gate nor state """
        gate = GateNor(self.sim)
        gate.inputs = []
        gate.update()
        gate.inputs.append(self.sw1)
        gate.inputs.append(self.sw2)
        self.sw1.state = 0
        self.sw2.state = 0
        gate.update()
        res1 = gate.state
        self.sw2.state = 1
        gate.update()
        res2 = gate.state
        self.sw1.state = 1
        gate.update()
        res3 = gate.state
        self.sw2.state = 0
        gate.update()
        res4 = gate.state
        self.assertEqual([res1, res2, res3, res4], [1, 0, 0, 0])

    def test_gate_xor(self):
        """ tasting gate xor state """
        gate = GateXor(self.sim)
        gate.inputs = []
        gate.update()
        gate.inputs.append(self.sw1)
        gate.inputs.append(self.sw2)
        self.sw1.state = 0
        self.sw2.state = 0
        gate.update()
        res1 = gate.state
        self.sw2.state = 1
        gate.update()
        res2 = gate.state
        self.sw1.state = 1
        gate.update()
        res3 = gate.state
        self.sw2.state = 0
        gate.update()
        res4 = gate.state
        self.assertEqual([res1, res2, res3, res4], [0, 1, 0, 1])

    def test_buffor(self):
        """ tasting buffor state """
        gate = GateBuffor(self.sim)
        gate.inputs = []
        gate.update()
        gate.inputs.append(self.sw1)
        self.sw1.state = 0
        gate.update()
        res1 = gate.state
        self.sw1.state = 1
        gate.update()
        res2 = gate.state
        self.assertEqual([res1, res2], [0, 1])

    def test_not(self):
        """ tasting gate not state """
        gate = GateNot(self.sim)
        gate.inputs = []
        gate.update()
        gate.inputs.append(self.sw1)
        self.sw1.state = 0
        gate.update()
        res1 = gate.state
        self.sw1.state = 1
        gate.update()
        res2 = gate.state
        self.assertEqual([res1, res2], [1, 0])

    def test_knot(self):
        """ tasting knot state """
        gate = Knot(self.sim)
        gate.inputs = []
        gate.update()
        gate.inputs.append(self.sw1)
        self.sw1.state = 0
        gate.update()
        res1 = gate.state
        self.sw1.state = 1
        gate.update()
        res2 = gate.state
        self.assertEqual([res1, res2], [0, 1])

    def test_bulb(self):
        """ tasting bulb state """
        gate = Bulb(self.sim)
        gate.inputs = []
        gate.update()
        gate.inputs.append(self.sw1)
        self.sw1.state = 0
        gate.update()
        res1 = gate.state
        self.sw1.state = 1
        gate.update()
        res2 = gate.state
        self.assertEqual([res1, res2], [0, 1])


TEST = unittest.TestLoader().loadTestsFromTestCase(TestGates)
print unittest.TextTestRunner(verbosity=True).run(TEST)

