""" Module with Game class """
import pygame
from wire import Wire
from gates import  GateAnd, GateOr, GateNand, GateNor, GateNot, GateXor, Bulb, Switch
from visualizers import Visualizer

class Simulator(object):
    """ Game class with main loop and event handling methods """
    CLEAR, GATE_SELECTED, WIRE_STARTED = range(3)

    def __init__(self):
        pygame.init() #inicjalizuje moduly
        self.running = True
        self.panels = {}
        self.vis = Visualizer(self)
        self.devices = {'gates' : pygame.sprite.Group(), 'switches' : pygame.sprite.Group(), 'bulbs' : pygame.sprite.Group(), 'wires' : []}
        self.current_device = None
        self.start_device = None
        self.cur_wire_state = self.CLEAR
        pygame.display.flip()

    def on_event(self, event):
        """ Events handling method """
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            if self.panels['devices_panel'].collidepoint(event.pos):
                self.choose_device_event(event.pos)
            elif self.panels['inside_main_panel'].collidepoint(event.pos):
                self.inside_main_panel_event(event.pos)
            elif self.panels['print_button'].collidepoint(event.pos):
                if self.cur_wire_state == self.CLEAR: #kursor pusty
                    panel = self.panels['main_panel']
                    image = "screen1.jpeg"
                    pygame.image.save(self.vis.screen.subsurface(panel), image)
            elif self.panels['clear_button'].collidepoint(event.pos):
                if self.cur_wire_state == self.CLEAR: #kursor pusty
                    self.devices['gates'] = pygame.sprite.Group()
                    self.devices['switches'] = pygame.sprite.Group()
                    self.devices['bulbs'] = pygame.sprite.Group()
                    self.devices['wires'] = []
                    self.current_device = None
                    self.cur_wire_state = self.CLEAR
        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
            self.remove_event(event.pos)

    def choose_device_event(self, pos):
        """ Left panel clicked """
        if self.cur_wire_state == self.CLEAR: #nic nie bylo na kursorze
            self.current_device = self.which_device_choosen(pos)
            self.cur_wire_state = self.GATE_SELECTED #bramka na kursorze
        else:
            if self.current_device != None:
                self.current_device.remove_from_group()
            self.current_device = None
            self.cur_wire_state = self.CLEAR

    def inside_main_panel_event(self, pos):
        """ Main panel clicked """
        if self.cur_wire_state == self.GATE_SELECTED: #bramkana kursorze
            self.place_device_event(pos)
        elif self.cur_wire_state == self.CLEAR: #kursor pusty
            self.main_panel_device_clicked_event(pos)
        elif self.cur_wire_state == self.WIRE_STARTED:
            self.wire_started_event(pos)

    def place_device_event(self, pos):
        """ Device is attached to the cursor, choose place on main panel to place it """
        pos_x, pos_y = pos
        self.current_device.remove_from_group() #usuwam tymczasowo
        self.current_device.rect.topleft = (pos_x - self.vis.ICON_W / 2, pos_y - self.vis.ICON_H / 2)

        if (pygame.sprite.spritecollideany(self.current_device, self.devices['gates']) in [None, self.current_device] and\
        pygame.sprite.spritecollideany(self.current_device, self.devices['bulbs']) in [None, self.current_device] and\
        pygame.sprite.spritecollideany(self.current_device, self.devices['switches']) in [None, self.current_device]):
            print "no collision"
            self.vis.screen.blit(self.current_device.icon, (pos_x - self.vis.ICON_W / 2, pos_y - self.vis.ICON_H / 2))
            pygame.display.flip()
            self.current_device.add_to_group() #dodaje z powrotem
            self.current_device = None
        else:
            print "collision found"
            self.current_device = None

        self.cur_wire_state = self.CLEAR

    def main_panel_device_clicked_event(self, pos):
        """ Click on deivce from main panel to start wire or change state """
        pos_x, pos_y = pos
        self.start_device = None
        for gate in self.devices['gates']:
            if gate.rects['move_rect'].collidepoint((pos_x, pos_y)):
                pass
                #gate.set_position(pos_x, pos_y)
            elif gate.rect.collidepoint((pos_x, pos_y)):
                self.start_device = gate
                break

        for switch in self.devices['switches']:
            if switch.rect.collidepoint((pos_x, pos_y)):
                if len(switch.outputs) > 0:
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
            self.cur_wire_state = self.WIRE_STARTED

    def wire_started_event(self, pos):
        """ Choose device to end wire """
        pos_x, pos_y = pos
        device_clicked = None
        for gate in self.devices['gates']:
            if gate.rect.collidepoint((pos_x, pos_y)) and len(gate.inputs) < gate.inputs_max:
                if gate != self.start_device:
                    device_clicked = gate
                    gate.inputs.append(self.start_device)
                    self.start_device.outputs.append(gate)
                    break

        for bulb in self.devices['bulbs']:
            if bulb.rect.collidepoint((pos_x, pos_y)) and len(bulb.inputs) < bulb.inputs_max:
                device_clicked = bulb
                bulb.inputs.append(self.start_device)
                self.start_device.outputs.append(bulb)
                break

        if device_clicked != None:
            end_device = device_clicked
            wire = Wire(self.start_device, end_device)
            self.devices['wires'].append(wire)
            print len(self.devices['wires'])
            self.cur_wire_state = self.CLEAR #kursor wolny

    def remove_event(self, pos):
        """ Right-click to remove device from panel """
        pos_x, pos_y = pos
        device_clicked = None
        for gate in self.devices['gates']:
            if gate.rect.collidepoint((pos_x, pos_y)):
                device_clicked = gate
                self.devices['gates'].remove(device_clicked)
                break

        for switch in self.devices['switches']:
            if switch.rect.collidepoint((pos_x, pos_y)):
                device_clicked = switch
                self.devices['switches'].remove(device_clicked)
                break

        for bulb in self.devices['bulbs']:
            if bulb.rect.collidepoint((pos_x, pos_y)):
                device_clicked = bulb
                self.devices['bulbs'].remove(device_clicked)
                break

        if device_clicked != None:
            print 'wires:', len(device_clicked.wires['wires'])
            for wire in device_clicked.wires['wires']:
                if wire in self.devices['wires']:
                    self.devices['wires'].remove(wire)
                if wire.start_gate == device_clicked:
                    end_device = wire.end_gate
                    end_device.wires['wires'].remove(wire)
                    end_device.wires['wires_ended'].remove(wire)
                    device_clicked.outputs.remove(end_device)
                    end_device.inputs.remove(device_clicked)
                else:
                    start_device = wire.start_gate
                    start_device.wires['wires'].remove(wire)
                    start_device.wires['wires_started'].remove(wire)
                    start_device.outputs.remove(device_clicked)
                    device_clicked.inputs.remove(start_device)

            device_clicked.wires['wires'] = []
            device_clicked.wires['wires_started'] = []
            print len(self.devices['wires'])

    def which_device_choosen(self, pos):
        """ Find out which device has been cliked on the left panel """
        if self.panels['devices_panel'].collidepoint(pos):
            pos_y = pos[1]
            if pos_y < self.panels['devices_panel'].top + self.vis.ICON_H:
                dev = GateAnd(self)
            elif pos_y < self.panels['devices_panel'].top + self.vis.ICON_H * 2:
                dev = GateOr(self)
            elif pos_y < self.panels['devices_panel'].top + self.vis.ICON_H * 3:
                dev = GateNand(self)
            elif pos_y < self.panels['devices_panel'].top + self.vis.ICON_H * 4:
                dev = GateNor(self)
            elif pos_y < self.panels['devices_panel'].top + self.vis.ICON_H * 5:
                dev = GateNot(self)
            elif pos_y < self.panels['devices_panel'].top + self.vis.ICON_H * 6:
                dev = GateXor(self)
            elif pos_y < self.panels['devices_panel'].top + self.vis.ICON_H * 7:
                dev = Switch(self)
            else:
                dev = Bulb(self)
            dev.add_to_group()
            return dev
        return None

    def run(self):
        """ Main loop """
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            pos_x, pos_y = pygame.mouse.get_pos()
            if self.current_device != None:
                self.current_device.rects['icon_rect'] = (pos_x - self.vis.ICON_W / 2, pos_y - self.vis.ICON_H / 2)
            self.vis.draw_background()
            pygame.display.flip()

        pygame.quit()
