""" Module containing unit tests """
import unittest
import sys
sys.path.append('..')
from main.main import Main
from main.simulator import Simulator
from devices.gates import GateAnd, Switch, GateOr, GateBuffor, GateNot,\
                          Bulb, Knot

class MultiGatesTest(unittest.TestCase):
    """ class with unittest methods """
    def setUp(self):
        """ set up initializations """
        self.my_main = Main()
        self.sim = Simulator(self.my_main)
        self.sw1 = Switch(self.sim)
        self.sw2 = Switch(self.sim)

    def test_circuit(self):
        """ tasting circuit state """
        bulb = Bulb(self.sim)
        buffor = GateBuffor(self.sim)
        gate_not = GateNot(self.sim)
        gate_or = GateOr(self.sim)
        gate_and = GateAnd(self.sim)
        knot = Knot(self.sim)

        bulb.inputs.append(buffor)
        buffor.inputs.append(gate_or)
        gate_or.inputs.append(knot)
        gate_or.inputs.append(gate_and)
        gate_and.inputs.append(knot)
        gate_and.inputs.append(gate_not)
        knot.inputs.append(self.sw1)
        gate_not.inputs.append(self.sw2)

        self.assertEqual([bulb.state], [0])

    def test_circuit2(self):
        """ tasting circuit state """
        bulb = Bulb(self.sim)
        buffor = GateBuffor(self.sim)
        gate_not = GateNot(self.sim)
        gate_or = GateOr(self.sim)
        gate_and = GateAnd(self.sim)
        knot = Knot(self.sim)

        bulb.inputs.append(buffor)
        buffor.inputs.append(gate_or)
        gate_or.inputs.append(knot)
        gate_or.inputs.append(gate_and)
        gate_and.inputs.append(knot)
        gate_and.inputs.append(gate_not)
        knot.inputs.append(self.sw1)
        gate_not.inputs.append(self.sw2)

        self.sw1.state = 1
        self.sw2.state = 1
        gate_not.update()
        knot.update()
        gate_and.update()
        gate_or.update()
        buffor.update()
        bulb.update()
        self.assertEqual([bulb.state], [1])

    def test_circuit3(self):
        """ tasting circuit state """
        bulb = Bulb(self.sim)
        buffor = GateBuffor(self.sim)
        gate_not = GateNot(self.sim)
        gate_or = GateOr(self.sim)
        gate_and = GateAnd(self.sim)
        knot = Knot(self.sim)

        bulb.inputs.append(buffor)
        buffor.inputs.append(gate_or)
        gate_or.inputs.append(knot)
        gate_or.inputs.append(gate_and)
        gate_and.inputs.append(knot)
        gate_and.inputs.append(gate_not)
        knot.inputs.append(self.sw1)
        gate_not.inputs.append(self.sw2)

        self.sw1.state = 1
        self.sw2.state = 0
        gate_not.update()
        knot.update()
        gate_and.update()
        gate_or.update()
        buffor.update()
        bulb.update()
        self.assertEqual([bulb.state], [1])

TEST = unittest.TestLoader().loadTestsFromTestCase(MultiGatesTest)
print unittest.TextTestRunner(verbosity=True).run(TEST)


