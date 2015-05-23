import pygame
from pygame.locals import *
from pygame.sprite import Sprite

class Device(Sprite):	
	
	ICON_WIDTH, ICON_HEIGHT = 116, 71
	
	def __init__(self, screen, game):
		Sprite.__init__(self)     
		self.screen = screen
		self.game = game
		self.state = 0
		self.wires = []
		
	def draw(self):
		self.screen.blit(self.icon, self.icon_rect)
		pygame.display.flip()
		self.update() 
	
	def icon_init(self, name):
		self.icon = pygame.image.load(name+".jpg").convert()
		self.icon_rect = self.icon.get_rect()
		self.rect = self.icon_rect

	def remove(self):
		pass	

class Gate(Device):	

	def __init__(self, screen, game):
		Device.__init__(self, screen, game)     
		self.inputs_max = 2	# poza not
		self.inputs = []
		self.outputs = []
		self.wires_ended = []
		self.wires_started = []
			
	def remove_from_group(self):
		self.game.gates.remove(self)
		
	def add_to_group(self):
		self.game.gates.add(self)	
		
	def remove(self):
		pass	
	
	def wire_begin_pos(self):
		return (self.rect.right, int(self.rect.top + self.ICON_HEIGHT / 2))
		
	def wire_end_pos(self): 
		return [(self.rect.left, int(self.rect.top + self.ICON_HEIGHT / 3.)-8), 	#poza not
				(self.rect.left, int(self.rect.top + self.ICON_HEIGHT)-16)]	
	
	def add_started_wire(self, wire):	
		self.wires_started.append(wire)
		self.wires.append(wire)
				
	def add_ended_wire(self, wire):
		self.wires_ended.append(wire)	
		self.wires.append(wire)
						
class GateAnd(Gate):
	
	def __init__(self, screen, game):
		Gate.__init__(self, screen, game)      
		self.icon_init("icons/and")
	
	def update(self):
		self.state = 0
		if len(self.inputs) > 1:	
			if self.inputs[0].state == 1 and self.inputs[1].state == 1:
				self.state = 1
			else:
				self.state = 0	
	
class GateOr(Gate):	
	
	def __init__(self, screen, game):
		Gate.__init__(self, screen, game)      
		self.icon_init("icons/or")
	
	def update(self):	
		self.state = 0
		if len(self.inputs) > 1:	
			if self.inputs[0].state == 0 and self.inputs[1].state == 0:
				self.state = 0
			else:
				self.state = 1	
	
class GateNot(Gate):
	
	def __init__(self, screen, game):
		Gate.__init__(self, screen, game)      
		self.icon_init("icons/not")
		self.inputs_max = 1
	
	def update(self):
		self.state = 0	
		if len(self.inputs) > 0:	
			self.state = (self.inputs[0].state +1) % 2
				
	def wire_end_pos(self): 
		return [(self.rect.left, int(self.rect.top + self.ICON_HEIGHT / 2))]
	
class GateNand(Gate):
	
	def __init__(self, screen, game):
		Gate.__init__(self, screen, game)      
		self.icon_init("icons/nand")
	
	def update(self):	
		self.state = 0
		if len(self.inputs) > 1:	
			if self.inputs[0].state == 1 and self.inputs[1].state == 1:
				self.state = 0
			else:
				self.state = 1		
	
class GateNor(Gate):
	
	def __init__(self, screen, game):
		Gate.__init__(self, screen, game)      
		self.icon_init("icons/nor")
		
	def update(self):
		self.state = 0	
		if len(self.inputs) > 1:	
			if self.inputs[0].state == 0 and self.inputs[1].state == 0:
				self.state = 1
			else:
				self.state = 0		
	
class GateXor(Gate):
	
	def __init__(self, screen, game):
		Gate.__init__(self, screen, game)      
		self.icon_init("icons/xor")
		
	def update(self):	
		self.state = 0
		if len(self.inputs) > 1:	
			if self.inputs[0].state ==  self.inputs[1].state:
				self.state = 0
			else:
				self.state = 1		
	
class Bulb(Device):

	def __init__(self, screen, game):   
		Device.__init__(self, screen, game)     
		self.icon_init("icons/bulb0")		
		self.icon0 = pygame.image.load("icons/bulb0.jpg").convert()
		self.icon0_rect = self.icon0.get_rect()
		self.icon1 = pygame.image.load("icons/bulb1.jpg").convert()
		self.icon1_rect = self.icon1.get_rect()
		self.inputs = []
		self.inputs_max = 1
		self.wires_started = []	#puste
		self.wires_ended = []
		
	def update(self):
		self.state = 0
		if len(self.inputs) > 0:	
			self.state = self.inputs[0].state
		if self.state == 1:
			self.icon = self.icon1
		else:
			self.icon = self.icon0	
	
	def remove_from_group(self):
		self.game.bulbs.remove(self)
		
	def add_to_group(self):
		self.game.bulbs.add(self)	
			
	def wire_end_pos(self): 
		return [(self.rect.left, self.rect.top + int(self.ICON_HEIGHT / 2))]	   
				
	def add_ended_wire(self, wire):
		self.wires_ended.append(wire)	
		self.wires.append(wire)   	
	
class Switch(Device):
	
	def __init__(self, screen, game):   
		Device.__init__(self, screen, game)
		self.icon_init("icons/switch0")
		self.icon0 = pygame.image.load("icons/switch0.jpg").convert()
		self.icon0_rect = self.icon0.get_rect()
		self.icon1 = pygame.image.load("icons/switch1.jpg").convert()
		self.icon1_rect = self.icon1.get_rect()
		self.outputs = []
		self.wires_ended = []	#puste
		self.wires_started = []
		
	def update(self,mx,my):	
		self.state = 0
		if self.state == 1:
			self.icon_init("icons/switch1")			
			self.icon_rect = self.icon.get_rect()
			self.rect = self.icon_rect
		
	def remove_from_group(self):
		self.game.switches.remove(self)
	
	def add_to_group(self):
		self.game.switches.add(self)
			
	def wire_begin_pos(self): 
		return (self.rect.right, int(self.rect.top + self.ICON_HEIGHT / 2))
	
	def add_started_wire(self, wire):	
		self.wires_started.append(wire)
		self.wires.append(wire)
				
