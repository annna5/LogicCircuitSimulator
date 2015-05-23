import pygame
from pygame.locals import *
from wire import Wire
from gates import *

class Game(object):
	
	SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
	ICON_WIDTH, ICON_HEIGHT = 116, 71   
	ITEMS_ICONS = ['and.jpg','or.jpg','nand.jpg','nor.jpg','not.jpg','xor.jpg','switch0.jpg','bulb0.jpg']
	CLEAR, GATE_SELECTED, GATE_PUT, WIRE_STARTED = range(4)
	BLACK, BLUE = (0, 0, 0), (83,126,139)
	
	def __init__(self):
		pygame.init()		#inicjalizuje moduly
		self.running = True
		self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
		pygame.display.flip()
		
		self.gates = pygame.sprite.Group()
		self.switches = pygame.sprite.Group()
		self.bulbs = pygame.sprite.Group()
		self.wires = []	
		self.current_device = None
		self.cur_wire_state = self.CLEAR
		
		self.images = []
		for i in range(len(self.ITEMS_ICONS)):
			icon = pygame.image.load("icons/"+self.ITEMS_ICONS[i]).convert()
			self.images.append(icon)
        
	def on_event(self, event):		
		if event.type == pygame.QUIT:
			self.running = False
			
		elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:	
			mx, my = event.pos
			# panel po lewej
			if event.pos[0] < self.ICON_WIDTH and event.pos[1] < self.ICON_HEIGHT * len(self.ITEMS_ICONS):	#zmienic na in select_area
				if self.cur_wire_state == self.CLEAR:		#nic nie bylo na kursorze
					self.current_device = self.which_device_choosen(event.pos)
					self.cur_wire_state = self.GATE_SELECTED	#bramka na kursorze
				else:
					if self.current_device != None:
						self.current_device.remove_from_group()
					self.current_device = None	
					self.cur_wire_state = self.CLEAR
			else:	#poza obszarem wyboru
				if self.cur_wire_state == self.GATE_SELECTED:	#jest bramka na kursorze	
					self.current_device.remove_from_group()	#usuwam tymczasowo
					self.current_device.rect.topleft = (mx - self.ICON_WIDTH / 2, my - self.ICON_HEIGHT / 2)
					#zamienic na funkcje
					if (pygame.sprite.spritecollideany(self.current_device, self.gates) == None or\
					    pygame.sprite.spritecollideany(self.current_device, self.gates) == self.current_device) and\
					   (pygame.sprite.spritecollideany(self.current_device, self.bulbs) == None or\
					    pygame.sprite.spritecollideany(self.current_device, self.bulbs) == self.current_device)and\
					   (pygame.sprite.spritecollideany(self.current_device, self.switches) == None or\
					    pygame.sprite.spritecollideany(self.current_device, self.switches) == self.current_device):
						print "no collision"
						self.screen.blit(self.current_device.icon, (mx - self.ICON_WIDTH / 2, my - self.ICON_HEIGHT / 2))
						pygame.display.flip()
						self.current_device.add_to_group()	#dodaje z powrotem
						self.current_device = None					
					else:
						print "collision found"
						self.current_device = None
					self.cur_wire_state = self.CLEAR
					
				elif self.cur_wire_state == self.CLEAR: #nie ma bramki na kursorze
					self.start_device = None
					for gate in self.gates:
						if gate.rect.collidepoint((mx, my)):
							self.start_device = gate
							break						
					for switch in self.switches:
						if switch.rect.collidepoint((mx, my)):
							if len(switch.outputs) > 0:		# to zmienia stan,     ZMIENIC NA FUNKCJE
								if switch.state == 0:
									switch.state = 1
									switch.icon = switch.icon1
								else:
									switch.state = 0
									switch.icon = switch.icon0	
							else:	
								self.start_device = switch
							break					
							
					if self.start_device != None:
						self.cur_wire_state = self.WIRE_STARTED	#kabel rozpoczety	
						print "wire started"			
						
				elif self.cur_wire_state == self.WIRE_STARTED:
					device_clicked = None
					for gate in self.gates:
						if gate.rect.collidepoint((mx, my)) and len(gate.inputs) < gate.inputs_max: 
							if gate != self.start_device:
								device_clicked = gate
								gate.inputs.append(self.start_device)
								self.start_device.outputs.append(gate)
								break
					for bulb in self.bulbs:
						if bulb.rect.collidepoint((mx, my)) and len(bulb.inputs) < bulb.inputs_max: 
							device_clicked = bulb
							bulb.inputs.append(self.start_device)
							self.start_device.outputs.append(bulb)
							break			
							
					if device_clicked != None:
						self.end_device = device_clicked
						wire = Wire(self.start_device, self.end_device)
						self.wires.append(wire)
						wire.finish_wire_here(self.end_device)	
						self.cur_wire_state = self.CLEAR	#kursor wolny
				
		elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]: #usuwanie
			mx, my = event.pos	
			device_clicked = None
			for gate in self.gates:
				if gate.rect.collidepoint((mx, my)):
					device_clicked = gate
					self.gates.remove(device_clicked)
					break
					
			for switch in self.switches:
				if switch.rect.collidepoint((mx, my)):
					device_clicked = switch
					self.switches.remove(device_clicked)
					break
			
			for bulb in self.bulbs:
				if bulb.rect.collidepoint((mx, my)):
					device_clicked = bulb
					self.bulbs.remove(device_clicked)
					break
							
			if device_clicked != None:
				for wire in device_clicked.wires:
					wire.remove()
					
					if wire in self.wires:		
						self.wires.remove(wire)
			
	def on_cleanup(self):
		pygame.quit()		#zamyka moduly
			
	def run(self):

		while(self.running):
			for event in pygame.event.get():
				self.on_event(event)
			mx, my = pygame.mouse.get_pos()		
			if self.current_device != None:
				self.current_device.icon_rect = (mx - self.ICON_WIDTH / 2, my - self.ICON_HEIGHT / 2)
			self.draw_background()
			pygame.display.flip()
		#pygame.image.save(self.screen, "screen.jpeg")				
		self.on_cleanup()

	def which_device_choosen(self, pos):
		if pos[0] < self.ICON_WIDTH and pos[1] < self.ICON_HEIGHT * len(self.ITEMS_ICONS):
			if Rect((0, 0, self.ICON_WIDTH, self.ICON_HEIGHT)).collidepoint(pos):
				g = GateAnd(self.screen, self)
			elif Rect((0, self.ICON_HEIGHT, self.ICON_WIDTH, self.ICON_HEIGHT)).collidepoint(pos):
				g = GateOr(self.screen, self)
			elif Rect((0, self.ICON_HEIGHT * 2, self.ICON_WIDTH, self.ICON_HEIGHT)).collidepoint(pos):
				g = GateNand(self.screen, self)
			elif Rect((0, self.ICON_HEIGHT * 3, self.ICON_WIDTH, self.ICON_HEIGHT)).collidepoint(pos):
				g = GateNor(self.screen, self)
			elif Rect((0, self.ICON_HEIGHT * 4, self.ICON_WIDTH, self.ICON_HEIGHT)).collidepoint(pos):
				g = GateNot(self.screen, self)
			elif Rect((0, self.ICON_HEIGHT * 5, self.ICON_WIDTH, self.ICON_HEIGHT)).collidepoint(pos):
				g = GateXor(self.screen, self)
			elif Rect((0, self.ICON_HEIGHT * 6, self.ICON_WIDTH, self.ICON_HEIGHT)).collidepoint(pos):
				g = Switch(self.screen, self)
			elif Rect((0, self.ICON_HEIGHT * 7, self.ICON_WIDTH, self.ICON_HEIGHT)).collidepoint(pos):
				g = Bulb(self.screen, self)
			g.add_to_group()	
			return g
		return None		
		
	def draw_background(self):
		self.screen.fill(self.BLACK)
		for i in range(len(self.ITEMS_ICONS)):
			img_rect = self.images[i].get_rect()
			img_rect.topleft = (0, i * img_rect.height)					
			self.screen.blit(self.images[i], img_rect)
		for gate in self.gates:
			gate.update()
			self.screen.blit(gate.icon, gate.icon_rect)
		for switch in self.switches:
			#switch.update()
			self.screen.blit(switch.icon, switch.icon_rect)
		for bulb in self.bulbs:
			bulb.update()
			self.screen.blit(bulb.icon, bulb.icon_rect)
		for wire in self.wires:
			if wire.end_gate != None:
				wire.draw(self.screen)	
			else:
				print "error here"	
	
if __name__ == "__main__" :
    g = Game()
    g.run()		
