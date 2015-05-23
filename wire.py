import pygame
import pygame.gfxdraw

class Wire(object):
	BLUE =  (83,126,139)
	def __init__(self, start_gate, end_gate):
		self.start_gate = start_gate
		self.end_gate = end_gate
		start_gate.add_started_wire(self)
		end_gate.add_ended_wire(self)
	
	def start_wire_here(self, start_gate):
		self.start_gate = start_gate
		self.wire_started = True
		self.wire_finished = False
		
	def finish_wire_here(self, end_gate):
		self.end_gate = end_gate
		self.wire_started = False
		self.wire_finished = True
		
		
	def draw(self, screen):
		pygame.draw.line(screen, self.BLUE, self.start_gate.wire_begin_pos(), (self.end_gate.wire_end_pos())[self.end_gate.inputs.index(self.start_gate)], 4)

	def remove(self):
		st = self.start_gate
		en = self.end_gate
		st.wires.remove(self)
		st.wires_started.remove(self)
		en.wires.remove(self)
		en.wires_ended.remove(self)
		st.outputs.remove(en)
		en.inputs.remove(st)
		#usunac 
		


