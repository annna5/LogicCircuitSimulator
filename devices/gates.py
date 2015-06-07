""" Module contains all Devices types """
import pygame
import os, inspect, sys
from pygame.sprite import Sprite
CMD_FOLDER = os.path.realpath(os.path.abspath(os.path.split(\
                inspect.getfile(inspect.currentframe()))[0]))
if CMD_FOLDER not in sys.path:
    sys.path.insert(0, CMD_FOLDER)
class Device(Sprite):
    """ Parent device class """
    ICON_W, ICON_H = 100, 63

    def __init__(self, simulator):
        Sprite.__init__(self)
        self.simulator = simulator
        self.state = 0
        wires = []
        wires_ended = []
        wires_started = []
        self.wires = {'wires' : wires, 'wires_ended' :wires_ended,\
                      'wires_started' :wires_started}
        self.rects = {'icon_rect' : None, 'move_rect' : None}
        self.icon = None
        self.rect = None

    def draw(self):
        """ Draw device icon """
        self.simulator.vis.screen.blit(self.icon, self.rects['icon_rect'])
        pygame.display.flip()
        self.update()

    def icon_init(self, name):
        """ Initialize device icon """
        self.icon = pygame.image.load(os.path.join(os.path.dirname(CMD_FOLDER),\
                    "visualizers/icons/"+name+".jpg")).convert()
        self.rects['icon_rect'] = self.icon.get_rect()
        self.rect = self.rects['icon_rect']
        self.rects['move_rect'] = pygame.Rect(self.rect.left,\
                                              self.rect.top, 15, 15)

class Gate(Device):
    """ Class represents all gates types """
    def __init__(self, simulator):
        Device.__init__(self, simulator)
        self.inputs_max = 2    # poza not
        self.inputs = []
        self.outputs = []

    def remove_from_group(self):
        """ Remove gate from sprite group """
        self.simulator.devices['gates'].remove(self)

    def add_to_group(self):
        """ Add gate to sprite group """
        self.simulator.devices['gates'].add(self)

    def wire_begin_pos(self):
        """ Calculate posistion where wire starts """
        return (self.rect.right, int(self.rect.top + self.ICON_H / 2))

    def wire_end_pos(self):
        """ Calculate posistion where wire ends """
        return [(self.rect.left, int(self.rect.top + self.ICON_H / 3.)-8),
                (self.rect.left, int(self.rect.top + self.ICON_H)-14)]

    def add_started_wire(self, wire):
        """ Add wire to gate lists """
        self.wires['wires_started'].append(wire)
        self.wires['wires'].append(wire)

    def add_ended_wire(self, wire):
        """ Add wire to gate lists """
        self.wires['wires_ended'].append(wire)
        self.wires['wires'].append(wire)

    def remove_wires(self):
        """ Clear wires lists after removing device """
        self.wires['wires'] = []
        self.wires['wires_ended'] = []
        self.wires['wires_started'] = []

class GateAnd(Gate):
    """ Gate represents logical conjunction """
    def __init__(self, simulator):
        Gate.__init__(self, simulator)
        self.icon_init("and")

    def update(self):
        """ Updates gate state """
        self.state = 0
        if len(self.inputs) > 1:
            if self.inputs[0].state == 1 and self.inputs[1].state == 1:
                self.state = 1
            else:
                self.state = 0

class GateOr(Gate):
    """ Gate represents logical disjunction """
    def __init__(self, simulator):
        Gate.__init__(self, simulator)
        self.icon_init("or")

    def update(self):
        """ Updates gate state """
        self.state = 0
        if len(self.inputs) > 1:
            if self.inputs[0].state == 0 and self.inputs[1].state == 0:
                self.state = 0
            else:
                self.state = 1

class GateNot(Gate):
    """ Gate represents logical Negation """
    def __init__(self, simulator):
        Gate.__init__(self, simulator)
        self.icon_init("not")
        self.inputs_max = 1

    def update(self):
        """ Updates gate state """
        self.state = 0
        if len(self.inputs) > 0:
            self.state = (self.inputs[0].state +1) % 2

    def wire_end_pos(self):
        return [(self.rect.left, int(self.rect.top + self.ICON_H / 2)-1)]

class GateBuffor(Gate):
    """ Buffor """
    def __init__(self, simulator):
        Gate.__init__(self, simulator)
        self.icon_init("buffor")
        self.inputs_max = 1

    def update(self):
        """ Updates gate state """
        self.state = 0
        if len(self.inputs) > 0:
            self.state = (self.inputs[0].state)

    def wire_end_pos(self):
        return [(self.rect.left, int(self.rect.top + self.ICON_H / 2)-1)]

class GateNand(Gate):
    """ Gate represents nand operation """
    def __init__(self, simulator):
        Gate.__init__(self, simulator)
        self.icon_init("nand")

    def update(self):
        """ Updates gate state """
        self.state = 0
        if len(self.inputs) > 1:
            if self.inputs[0].state == 1 and self.inputs[1].state == 1:
                self.state = 0
            else:
                self.state = 1

class GateNor(Gate):
    """ Gate represents logical nor """
    def __init__(self, simulator):
        Gate.__init__(self, simulator)
        self.icon_init("nor")

    def update(self):
        """ Updates gate state """
        self.state = 0
        if len(self.inputs) > 1:
            if self.inputs[0].state == 0 and self.inputs[1].state == 0:
                self.state = 1
            else:
                self.state = 0

class GateXor(Gate):
    """ Gate represents logical exclusive or """
    def __init__(self, simulator):
        Gate.__init__(self, simulator)
        self.icon_init("xor")

    def update(self):
        """ Updates gate state """
        self.state = 0
        if len(self.inputs) > 1:
            if self.inputs[0].state == self.inputs[1].state:
                self.state = 0
            else:
                self.state = 1

class Bulb(Device):
    """ Represents circuit output """
    def __init__(self, simulator):
        Device.__init__(self, simulator)
        self.icon_init("bulb0")
        self.icon0 = pygame.image.load(os.path.join(os.path.dirname(\
                     CMD_FOLDER), "visualizers/icons/bulb0.jpg")).convert()
        self.icon1 = pygame.image.load(os.path.join(os.path.dirname(\
                     CMD_FOLDER), "visualizers/icons/bulb1.jpg")).convert()
        self.inputs = []
        self.inputs_max = 1

    def update(self):
        """ Updates gate state """
        self.state = 0
        if len(self.inputs) > 0:
            self.state = self.inputs[0].state
        if self.state == 1:
            self.icon = self.icon1
        else:
            self.icon = self.icon0

    def remove_from_group(self):
        """ Removes bulb from its sprite group """
        self.simulator.devices['bulbs'].remove(self)

    def add_to_group(self):
        """ Add bulb to its sprite group """
        self.simulator.devices['bulbs'].add(self)

    def wire_end_pos(self):
        """ Calculate posistion where wire ends """
        return [(self.rect.left, self.rect.top + int(self.ICON_H / 2))]

    def add_ended_wire(self, wire):
        """ Add wire to gate lists """
        self.wires['wires_ended'].append(wire)
        self.wires['wires'].append(wire)

    def remove_wires(self):
        """ Clear wires lists after removing bulb """
        self.wires['wires'] = []
        self.wires['wires_ended'] = []

class Switch(Device):
    """ Represents circuit input """
    def __init__(self, simulator):
        Device.__init__(self, simulator)
        self.icon_init("switch0")
        self.icon0 = pygame.image.load(os.path.join(os.path.dirname(\
                     CMD_FOLDER), "visualizers/icons/switch0.jpg")).convert()
        self.icon1 = pygame.image.load(os.path.join(os.path.dirname(\
                     CMD_FOLDER), "visualizers/icons/switch1.jpg")).convert()
        self.outputs = []

    def update(self):
        """ Updates gate state """
        self.state = 0
        if self.state == 1:
            self.icon_init("switch1")
            self.rects['icon_rect'] = self.icon.get_rect()
            self.rect = self.rects['icon_rect']

    def remove_from_group(self):
        """ Removes switch from its sprite group """
        self.simulator.devices['switches'].remove(self)

    def add_to_group(self):
        """ Add bulb to its sprite group """
        self.simulator.devices['switches'].add(self)

    def wire_begin_pos(self):
        """ Calculate posistion where wire starts """
        return (self.rect.right, int(self.rect.top + self.ICON_H / 2) - 1)

    def add_started_wire(self, wire):
        """ Add wire to gate lists """
        self.wires['wires_started'].append(wire)
        self.wires['wires'].append(wire)

    def remove_wires(self):
        """ Clear wires lists after removing switch """
        self.wires['wires'] = []
        self.wires['wires_started'] = []

class Knot(Gate):
    """ Gate represents logical Negation """
    def __init__(self, simulator):
        Gate.__init__(self, simulator)
        self.icon_init("knot")
        self.inputs_max = 1

    def update(self):
        """ Updates gate state """
        self.state = 0
        if len(self.inputs) > 0:
            self.state = (self.inputs[0].state)

    def wire_end_pos(self):
        return [(self.rect.left, int(self.rect.top + self.ICON_H / 2)-1)]

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
