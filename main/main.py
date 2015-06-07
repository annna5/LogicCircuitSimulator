""" Module with main loop """
import pygame
import sys
sys.path.append('..')

from LogicCircuitSimulator.main.simulator import Simulator

class Main(object):
    """ class with main loop """
    def __init__(self):
        self.sim = Simulator(self)
    def run(self):
        """ Main loop """
        while self.sim.running:
            for event in pygame.event.get():
                self.sim.on_event(event)
            self.center_icon()
            self.sim.vis.draw_background()
            pygame.display.flip()

        pygame.quit()

    def center_icon(self):
        """ set cursor pos to icon center """
        pos_x, pos_y = pygame.mouse.get_pos()
        if self.sim.tmp_devices['current_device'] != None:
            self.sim.tmp_devices['current_device'].rects['icon_rect'] = \
                           (pos_x - self.sim.vis.ICON_W / 2,\
                            pos_y - self.sim.vis.ICON_H / 2)

