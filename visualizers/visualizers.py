""" Module with class Visualizer"""
import pygame
import os, inspect, sys
CMD_FOLDER = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(\
                              inspect.currentframe()))[0]))
if CMD_FOLDER not in sys.path:
    sys.path.insert(0, CMD_FOLDER)

CMD_SUBFOLDER = os.path.realpath(os.path.abspath(os.path.join(os.path.split(\
                     inspect.getfile(inspect.currentframe()))[0], "icons")))
if CMD_SUBFOLDER not in sys.path:
    sys.path.insert(0, CMD_SUBFOLDER)

class Visualizer(object):
    """ Class containng drawing methods"""
    SCREEN_W, SCREEN_H = 1300, 700
    ICON_W, ICON_H = 100, 63
    ICONS = ['and.jpg', 'or.jpg', 'nand.jpg', 'nor.jpg', 'buffor.jpg',\
             'not.jpg', 'xor.jpg', 'switch0.jpg', 'bulb0.jpg', 'knot.jpg']
    BLACK, WHITE = (0, 0, 0), (255, 255, 255)
    BLUE, BLUE2 = (83, 126, 139), (184, 225, 227)
    GRAY, GRAY2, GRAY3 = (64, 64, 64), (54, 54, 54), (32, 32, 32)
    H_MARGIN = 30
    V_MARGIN = 20
    SPACE = 14
    BUTTON_W, BUTTON_H = 116, 40

    def __init__(self, simulator):
        self.draw_st_panel = True
        self.screen = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        self.simulator = simulator

        main_panel_height = self.SCREEN_H - 2 * self.H_MARGIN
        left_panel_width = self.ICON_W + self.SPACE
        main_panel_width = self.SCREEN_W  - left_panel_width -\
                           self.BUTTON_W - self.V_MARGIN * 4
        main_panel = pygame.Rect(left_panel_width + self.V_MARGIN * 2,\
                                 self.H_MARGIN, main_panel_width,\
                                 main_panel_height)
        inside_main_panel = pygame.Rect(main_panel.left + self.ICON_W / 2 + 2,\
                                        main_panel.top + self.ICON_H / 2 + 2,\
                                        main_panel_width - self.ICON_W - 2,\
                                        main_panel_height - self.ICON_H - 2)
        self.simulator.panels = {\
          'main_panel' : main_panel,\
          'inside_main_panel' : inside_main_panel,\
          'start_panel': pygame.Rect(
                           left_panel_width + self.V_MARGIN * 2,\
                           self.H_MARGIN, main_panel_width, main_panel_height),\
          'help_button': pygame.Rect(
                             self.SCREEN_W - self.V_MARGIN - self.BUTTON_W,\
                             self.H_MARGIN, self.BUTTON_W, self.BUTTON_H),\
          'start_button':pygame.Rect(
                             left_panel_width + self.V_MARGIN * 2 +\
                             main_panel_width/2-90,\
                             self.H_MARGIN + main_panel_height - 90, 180, 60),\
          'left_panel' : pygame.Rect(
                             self.V_MARGIN, self.H_MARGIN -4,\
                             left_panel_width, main_panel_height),\
          'devices_panel' : pygame.Rect(
                             self.V_MARGIN + self.SPACE / 2, self.H_MARGIN+4,\
                             self.ICON_W, self.ICON_H * len(self.ICONS)),\
          'clear_button' : pygame.Rect(
                             self.SCREEN_W - self.V_MARGIN - self.BUTTON_W,\
                             self.SCREEN_H - self.H_MARGIN - self.BUTTON_H,\
                             self.BUTTON_W, self.BUTTON_H),\
          'print_button' : pygame.Rect(
                             self.SCREEN_W - self.V_MARGIN - self.BUTTON_W,\
                             self.SCREEN_H - self.H_MARGIN - self.SPACE -\
                             self.BUTTON_H * 2, self.BUTTON_W, self.BUTTON_H)}

        self.images = []
        for i in range(len(self.ICONS)):
            icon = pygame.image.load(os.path.join(CMD_FOLDER,\
                                "icons/"+ self.ICONS[i])).convert()
            self.images.append(icon)

    def draw_background(self):
        """ Draws window background """
        tile_img = pygame.image.load(os.path.join(CMD_FOLDER,\
                                    "background/2.png")).convert()
        img_rect = tile_img.get_rect()
        nrows = int(self.SCREEN_H / img_rect.height) + 1
        ncols = int(self.SCREEN_W  / img_rect.width) + 1

        for row in range(nrows):
            for col in range(ncols):
                img_rect.topleft = (col * img_rect.width, row * img_rect.height)
                self.screen.blit(tile_img, img_rect)

        self.draw_rects()
        self.draw_buttons()
        self.draw_icons()
        if self.draw_st_panel == True:
            self.draw_start_panel()

    def draw_rects(self):
        """ Draws panels """
        pygame.draw.rect(self.screen, self.BLACK,\
                         self.simulator.panels['left_panel'])
        pygame.draw.rect(self.screen, self.GRAY3,\
                         self.simulator.panels['left_panel'], 4)
        pygame.draw.rect(self.screen, self.BLACK,\
                         self.simulator.panels['main_panel'])
        pygame.draw.rect(self.screen, self.GRAY3,\
                         self.simulator.panels['main_panel'], 4)

    def draw_buttons(self):
        """ Draws buttons """
        pygame.draw.rect(self.screen, self.GRAY2,\
                         self.simulator.panels['clear_button'])
        pygame.draw.rect(self.screen, self.GRAY3,\
                         self.simulator.panels['clear_button'], 4)
        pygame.draw.rect(self.screen, self.GRAY2,\
                         self.simulator.panels['print_button'])
        pygame.draw.rect(self.screen, self.GRAY3,\
                         self.simulator.panels['print_button'], 4)
        pygame.draw.rect(self.screen, self.GRAY2,\
                         self.simulator.panels['help_button'])
        pygame.draw.rect(self.screen, self.GRAY3,\
                         self.simulator.panels['help_button'], 4)

        myfont = pygame.font.SysFont("monospace", 30)
        myfont.set_bold(True)

        buttons_msg = {
                    'clear_button_msg' : myfont.render("CLEAR", 1, self.BLACK),
                    'print_button_msg' : myfont.render("PRINT", 1, self.BLACK),
                    'help_button_msg' : myfont.render("HELP", 1, self.BLACK)}
        clear_button_text = pygame.Rect(\
                self.simulator.panels['clear_button'].left + 4,\
                self.simulator.panels['clear_button'].top + 4,\
                self.BUTTON_W, self.BUTTON_H)
        self.screen.blit(buttons_msg['clear_button_msg'], clear_button_text)

        print_button_text = pygame.Rect(\
                self.simulator.panels['print_button'].left + 4,\
                self.simulator.panels['print_button'].top + 4,\
                self.BUTTON_W, self.BUTTON_H)
        self.screen.blit(buttons_msg['print_button_msg'], print_button_text)

        help_button_text = pygame.Rect(
                self.simulator.panels['help_button'].left + 14,\
                self.simulator.panels['help_button'].top + 4,\
                self.BUTTON_W, self.BUTTON_H)
        self.screen.blit(buttons_msg['help_button_msg'], help_button_text)

    def draw_icons(self):
        """ Draws left panel """
        for i in range(len(self.ICONS)):
            img_rect = self.images[i].get_rect()
            img_rect.topleft = (self.V_MARGIN + self.SPACE / 2,\
               self.simulator.panels['devices_panel'].top+i * img_rect.height)
            self.screen.blit(self.images[i], img_rect)
        for gate in self.simulator.devices['gates']:
            gate.update()
            self.screen.blit(gate.icon, gate.rects['icon_rect'])
        for switch in self.simulator.devices['switches']:
            self.screen.blit(switch.icon, switch.rects['icon_rect'])
        for bulb in self.simulator.devices['bulbs']:
            bulb.update()
            self.screen.blit(bulb.icon, bulb.rects['icon_rect'])
        for wire in self.simulator.devices['wires']:
            wire.draw(self.screen)

    def draw_start_panel(self):
        """ Draws start (help) window """
        myfont = pygame.font.SysFont("monospace", 48)
        myfont.set_bold(True)
        pygame.draw.rect(self.screen, self.BLACK,\
                         self.simulator.panels['start_panel'])
        pygame.draw.rect(self.screen, self.GRAY3,\
                         self.simulator.panels['start_panel'], 4)
        pygame.draw.rect(self.screen, self.GRAY2,\
                         self.simulator.panels['start_button'])
        pygame.draw.rect(self.screen, self.GRAY3,\
                         self.simulator.panels['start_button'], 4)
        start_button_text = pygame.Rect(\
                         self.simulator.panels['start_button'].left + 6,\
                         self.simulator.panels['start_button'].top + 6, 100, 80)
        start_button_msg = myfont.render("START", 1, self.BLACK)
        self.screen.blit(start_button_msg, start_button_text)
        help_img = pygame.image.load(os.path.join(CMD_FOLDER,\
                                     "background/help.png")).convert()
        img_rect = help_img.get_rect()
        img_rect.center = self.simulator.panels['start_panel'].center
        self.screen.blit(help_img, img_rect)

