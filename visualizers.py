""" Module with class Visualizer"""
import pygame
class Visualizer(object):
    """ Class containng drawing methods"""
    SCREEN_W, SCREEN_H = 1300, 700
    ICON_W, ICON_H = 116, 71
    ICONS = ['and.jpg', 'or.jpg', 'nand.jpg', 'nor.jpg', 'not.jpg', 'xor.jpg', 'switch0.jpg', 'bulb0.jpg']
    BLACK, BLUE, WHITE, BLUE2 = (0, 0, 0), (83, 126, 139), (255, 255, 255), (184, 225, 227)
    GRAY, GRAY2, GRAY3 = (64, 64, 64), (54, 54, 54), (32, 32, 32)
    H_MARGIN = 40
    V_MARGIN = 20
    SPACE = 14
    BUTTON_W, BUTTON_H = ICON_W, 40

    def __init__(self, simulator):
        self.draw_st_panel = True
        self.screen = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        self.simulator = simulator

        main_panel_height = self.SCREEN_H - 2 * self.H_MARGIN
        left_panel_width = self.ICON_W + self.SPACE
        left_panel = pygame.Rect(self.V_MARGIN, self.H_MARGIN, left_panel_width, main_panel_height)

        main_panel_width = self.SCREEN_W  - left_panel_width - self.BUTTON_W - self.V_MARGIN * 4
        main_panel = pygame.Rect(left_panel_width + self.V_MARGIN * 2,\
                                 self.H_MARGIN, main_panel_width, main_panel_height)
        inside_main_panel = pygame.Rect(main_panel.left + self.ICON_W / 2 + 2,\
                                        main_panel.top + self.ICON_H / 2 + 2,\
                                        main_panel_width - self.ICON_W - 2,\
                                        main_panel_height - self.ICON_H - 2)

        devices_panel = pygame.Rect(self.V_MARGIN + self.SPACE / 2, 60, self.ICON_W, self.ICON_H * 8)

        help_button = pygame.Rect(self.SCREEN_W - self.V_MARGIN - self.BUTTON_W,\
                                  self.H_MARGIN, self.BUTTON_W, self.BUTTON_H)
        clear_button = pygame.Rect(self.SCREEN_W - self.V_MARGIN - self.BUTTON_W,\
                                   self.SCREEN_H - self.H_MARGIN - self.BUTTON_H,\
                                   self.BUTTON_W, self.BUTTON_H)
        print_button = pygame.Rect(self.SCREEN_W - self.V_MARGIN - self.BUTTON_W,\
                                   self.SCREEN_H - self.H_MARGIN - self.SPACE - self.BUTTON_H * 2,
                                   self.BUTTON_W, self.BUTTON_H)

        start_panel = pygame.Rect(self.BUTTON_W + self.SPACE + self.V_MARGIN * 2,\
                                  self.H_MARGIN, main_panel_width, main_panel_height)
        start_button = pygame.Rect(start_panel.left + main_panel_width/2-90,\
                                   start_panel.bottom - 90, 180, 60)

        self.simulator.panels = {'start_panel':start_panel, 'help_button':help_button,\
                                 'start_button':start_button, 'main_panel' : main_panel,\
                                 'inside_main_panel' : inside_main_panel, 'left_panel' : left_panel,\
                                 'devices_panel' : devices_panel, 'clear_button' : clear_button,\
                                 'print_button' : print_button}
        self.images = []
        for i in range(len(self.ICONS)):
            icon = pygame.image.load("icons/"+self.ICONS[i]).convert()
            self.images.append(icon)

    def draw_background(self):
        """ Draws window background """
        tile_img = pygame.image.load("background/2.png").convert()
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
        pygame.draw.rect(self.screen, self.BLACK, self.simulator.panels['left_panel'])
        pygame.draw.rect(self.screen, self.GRAY3, self.simulator.panels['left_panel'], 4)
        pygame.draw.rect(self.screen, self.BLACK, self.simulator.panels['main_panel'])
        pygame.draw.rect(self.screen, self.GRAY3, self.simulator.panels['main_panel'], 4)

    def draw_buttons(self):
        """ Draws buttons """
        pygame.draw.rect(self.screen, self.GRAY2, self.simulator.panels['clear_button'])
        pygame.draw.rect(self.screen, self.GRAY3, self.simulator.panels['clear_button'], 4)
        pygame.draw.rect(self.screen, self.GRAY2, self.simulator.panels['print_button'])
        pygame.draw.rect(self.screen, self.GRAY3, self.simulator.panels['print_button'], 4)
        pygame.draw.rect(self.screen, self.GRAY2, self.simulator.panels['help_button'])
        pygame.draw.rect(self.screen, self.GRAY3, self.simulator.panels['help_button'], 4)
        myfont = pygame.font.SysFont("monospace", 30)
        myfont.set_bold(True)

        clear_button_text = pygame.Rect(self.simulator.panels['clear_button'].left + 4,\
                                        self.simulator.panels['clear_button'].top + 4,\
                                        self.BUTTON_W, self.BUTTON_H)
        clear_button_msg = myfont.render("CLEAR", 1, self.BLACK)
        self.screen.blit(clear_button_msg, clear_button_text)

        print_button_text = pygame.Rect(self.simulator.panels['print_button'].left + 4,\
                                        self.simulator.panels['print_button'].top + 4,\
                                        self.BUTTON_W, self.BUTTON_H)
        print_button_msg = myfont.render("PRINT", 1, self.BLACK)
        self.screen.blit(print_button_msg, print_button_text)

        help_button_text = pygame.Rect(self.simulator.panels['help_button'].left + 14,\
                                       self.simulator.panels['help_button'].top + 4,\
                                       self.BUTTON_W, self.BUTTON_H)
        help_button_msg = myfont.render("HELP", 1, self.BLACK)
        self.screen.blit(help_button_msg, help_button_text)

    def draw_icons(self):
        """ Draws left panel """
        for i in range(len(self.ICONS)):
            img_rect = self.images[i].get_rect()
            img_rect.topleft = (self.V_MARGIN + self.SPACE / 2, 60+i * img_rect.height)
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
        pygame.draw.rect(self.screen, self.BLACK, self.simulator.panels['start_panel'])
        pygame.draw.rect(self.screen, self.GRAY3, self.simulator.panels['start_panel'], 4)
        pygame.draw.rect(self.screen, self.GRAY2, self.simulator.panels['start_button'])
        pygame.draw.rect(self.screen, self.GRAY3, self.simulator.panels['start_button'], 4)
        start_button_text = pygame.Rect(self.simulator.panels['start_button'].left + 6,\
                                        self.simulator.panels['start_button'].top + 6, 100, 80)
        start_button_msg = myfont.render("START", 1, self.BLACK)
        self.screen.blit(start_button_msg, start_button_text)
        help_img = pygame.image.load("background/help.png").convert()
        img_rect = help_img.get_rect()
        img_rect.center = self.simulator.panels['start_panel'].center
        self.screen.blit(help_img, img_rect)

