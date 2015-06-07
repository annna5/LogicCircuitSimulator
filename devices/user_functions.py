""" function saved by user """
from gates import Gate

class UserFunction(Gate):
    """ class represents function saved by user """
    ICON_W, ICON_H = 50, 63
    def __init__(self, simulator, pos):
        Gate.__init__(self, simulator)
        self.pos = pos
        self.icon_init("userfun")
        self.switches_number = len(self.simulator.main.user_simulators[\
                                   self.pos].devices['switches'])
        self.inputs_max = self.switches_number
        self.outputs_max = 1

    def update(self):
        """ Updates gate state """
        self.switches_number = len(self.simulator.main.user_simulators[\
                                   self.pos].devices['switches'])
        self.inputs_max = self.switches_number
        self.outputs_max = 1
        if len(self.inputs) == self.switches_number:
            self.state = self.calculate_state()

    def remove_from_group(self):
        """ Remove gate from sprite group """
        self.simulator.devices['new_functions'].remove(self)

    def add_to_group(self):
        """ Add gate to sprite group """
        self.simulator.devices['new_functions'].add(self)

    def wire_end_pos(self):
        """ Calculate posistion where wire ends """
        return [(self.rect.left, int(self.rect.top + self.ICON_H / 2)),
                (self.rect.left, int(self.rect.top + self.ICON_H / 2))]

    def calculate_state(self):
        """ calculates state """
        for i, switch in enumerate(self.simulator.main.user_simulators[\
                                   self.pos].devices['switches']):
            switch.state = self.inputs[i].state
            self.recursive_update(switch)
        for item in self.simulator.main.user_simulators[\
                    self.pos].devices['bulbs']:
            item.update()
            return item.state

    def recursive_update(self, gate):
        """recursive method for state updating """
        tmp = gate
        if type(tmp).__name__ != 'Bulb':
            for item in tmp.outputs:
                item.update()
                self.recursive_update(item)
        else:
            return

