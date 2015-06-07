""" Module with class Wire """
import pygame

class Wire(object):
    """ Class represents wire object """
    BLUE = (83, 126, 139)
    def __init__(self, start_gate, end_gate):
        self.start_gate = start_gate
        self.end_gate = end_gate
        start_gate.add_started_wire(self)
        end_gate.add_ended_wire(self)

    def start_wire_here(self, start_gate):
        """ Set start gate """
        self.start_gate = start_gate

    def finish_wire_here(self, end_gate):
        """ Set end gate """
        self.end_gate = end_gate

    def draw(self, screen):
        """ Draw line between two devices """
        st_pos = self.start_gate.wire_begin_pos()
        gate_index = self.end_gate.inputs.index(self.start_gate)%2
        end_pos = (self.end_gate.wire_end_pos())[gate_index]
        pygame.draw.line(screen, self.BLUE, st_pos, end_pos, 4)

