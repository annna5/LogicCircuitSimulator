""" Module with Simulator class """
import pygame
import os, inspect, sys
CMD_FOLDER = os.path.realpath(os.path.abspath(os.path.split\
                       (inspect.getfile(inspect.currentframe()))[0]))
if CMD_FOLDER not in sys.path:
    sys.path.insert(0, CMD_FOLDER)
from visualizers.visualizers import Visualizer
from devices.wires import Wire
from devices.gates import  GateAnd, GateOr, GateNand,\
               GateNor, GateBuffor, GateNot, GateXor, Bulb, Switch, Knot
class Simulator(object):
    """ class with event handling methods """
    CLEAR, GATE_SELECTED, WIRE_STARTED = range(3)

    def __init__(self, main):
        pygame.init()
        self.main = main
        self.running = True
        self.panels = {}
        self.vis = Visualizer(self)
        self.devices = {'gates' : pygame.sprite.Group(),\
                        'switches' : pygame.sprite.Group(),\
                        'bulbs' : pygame.sprite.Group(), 'wires' : []}
        current_device = None
        start_device = None
        self.tmp_devices = {'current_device' : current_device,\
                            'start_device' : start_device}
        self.cur_wire_state = self.CLEAR
        pygame.display.flip()

    def on_event(self, event):
        """ Events handling method """
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and\
                           pygame.mouse.get_pressed()[0]:
            if self.panels['devices_panel'].collidepoint(event.pos) and\
                           self.vis.draw_st_panel == False:
                self.choose_device_event(event.pos)
            elif self.panels['start_button'].collidepoint(event.pos) and\
                           self.vis.draw_st_panel == True:
                self.vis.draw_st_panel = False
            elif self.panels['inside_main_panel'].collidepoint(event.pos)\
                              and self.vis.draw_st_panel == False:
                self.inside_main_panel_event(event.pos)
            elif (self.panels['help_button'].collidepoint(event.pos) or\
                 self.panels['print_button'].collidepoint(event.pos) or\
                 self.panels['clear_button'].collidepoint(event.pos)) and\
                 self.vis.draw_st_panel == False:
                self.buttons_event(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN and\
                           pygame.mouse.get_pressed()[2]\
                               and self.vis.draw_st_panel == False:
            self.remove_event(event.pos)

    def choose_device_event(self, pos):
        """ Left panel clicked """
        if self.cur_wire_state == self.CLEAR: #nic nie bylo na kursorze
            self.tmp_devices['current_device'] = self.which_device_choosen(pos)
            self.cur_wire_state = self.GATE_SELECTED #bramka na kursorze
        else:
            if self.tmp_devices['current_device'] != None:
                self.tmp_devices['current_device'].remove_from_group()
            self.tmp_devices['current_device'] = None
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
        """ Device is attached to the cursor,
            choose place on main panel to place it """
        pos_x, pos_y = pos
        self.tmp_devices['current_device'].remove_from_group()
        self.tmp_devices['current_device'].rect.topleft =\
                                          (pos_x - self.vis.ICON_W / 2,\
                                           pos_y - self.vis.ICON_H / 2)

        if (pygame.sprite.spritecollideany(\
                self.tmp_devices['current_device'], self.devices['gates'])\
                in [None, self.tmp_devices['current_device']] and\
            pygame.sprite.spritecollideany(\
                self.tmp_devices['current_device'], self.devices['bulbs'])\
                in [None, self.tmp_devices['current_device']] and\
            pygame.sprite.spritecollideany(\
                self.tmp_devices['current_device'], self.devices['switches'])\
                in [None, self.tmp_devices['current_device']]):
            self.vis.screen.blit(self.tmp_devices['current_device'].icon,\
                                (pos_x - self.vis.ICON_W / 2,\
                                 pos_y - self.vis.ICON_H / 2))
            pygame.display.flip()
            self.tmp_devices['current_device'].add_to_group()
            self.tmp_devices['current_device'] = None
        else:
            self.tmp_devices['current_device'] = None

        self.cur_wire_state = self.CLEAR

    def main_panel_device_clicked_event(self, pos):
        """ Click on deivce from main panel to start wire or change state """
        pos_x, pos_y = pos
        self.tmp_devices['start_device'] = None
        for gate in self.devices['gates']:
            if gate.rect.collidepoint((pos_x, pos_y)):
                self.tmp_devices['start_device'] = gate
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
                    self.tmp_devices['start_device'] = switch
                break

        if self.tmp_devices['start_device'] != None:
            self.cur_wire_state = self.WIRE_STARTED

    def wire_started_event(self, pos):
        """ Choose device to end wire """
        pos_x, pos_y = pos
        device_clicked = None
        for gate in self.devices['gates']:
            if gate.rect.collidepoint((pos_x, pos_y)) and\
                   len(gate.inputs) < gate.inputs_max:
                if gate != self.tmp_devices['start_device']:
                    device_clicked = gate
                    gate.inputs.append(self.tmp_devices['start_device'])
                    self.tmp_devices['start_device'].outputs.append(gate)
                    break
                else:
                    self.cur_wire_state = self.CLEAR
                    device_clicked = None
                    return

        for bulb in self.devices['bulbs']:
            if bulb.rect.collidepoint((pos_x, pos_y)) and\
                 len(bulb.inputs) < bulb.inputs_max:
                device_clicked = bulb
                bulb.inputs.append(self.tmp_devices['start_device'])
                self.tmp_devices['start_device'].outputs.append(bulb)
                break

        if device_clicked != None:
            end_device = device_clicked
            wire = Wire(self.tmp_devices['start_device'], end_device)
            self.devices['wires'].append(wire)
            self.cur_wire_state = self.CLEAR #kursor wolny

    def choose_device_to_remove(self, pos):
        """ which device was right-clicked """
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
        return device_clicked

    def remove_event(self, pos):
        """ Right-click to remove device from panel """
        device_clicked = self.choose_device_to_remove(pos)
        if device_clicked != None:
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
                dev = GateBuffor(self)
            elif pos_y < self.panels['devices_panel'].top + self.vis.ICON_H * 6:
                dev = GateNot(self)
            elif pos_y < self.panels['devices_panel'].top + self.vis.ICON_H * 7:
                dev = GateXor(self)
            elif pos_y < self.panels['devices_panel'].top + self.vis.ICON_H * 8:
                dev = Switch(self)
            elif pos_y < self.panels['devices_panel'].top + self.vis.ICON_H * 9:
                dev = Bulb(self)
            else:
                dev = Knot(self)
            dev.add_to_group()
            return dev
        return None

    def buttons_event(self, pos):
        """ button clicked """
        if self.panels['help_button'].collidepoint(pos) and\
                          self.vis.draw_st_panel == False:
            if self.cur_wire_state == self.CLEAR: #kursor pusty
                self.vis.draw_st_panel = True
        elif self.panels['print_button'].collidepoint(pos) and\
                          self.vis.draw_st_panel == False:
            if self.cur_wire_state == self.CLEAR: #kursor pusty
                panel = self.panels['main_panel']
                image = "screen1.jpeg"
                pygame.image.save(self.vis.screen.subsurface(panel), image)
        elif self.panels['clear_button'].collidepoint(pos) and\
                          self.vis.draw_st_panel == False:
            if self.cur_wire_state == self.CLEAR: #kursor pusty
                self.devices['gates'] = pygame.sprite.Group()
                self.devices['switches'] = pygame.sprite.Group()
                self.devices['bulbs'] = pygame.sprite.Group()
                self.devices['wires'] = []
                self.tmp_devices['current_device'] = None
                self.cur_wire_state = self.CLEAR


