import pygame.font
from settings import Settings

class Button():

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        self.width, self.height = 300, 100
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center
        self.clicked = False

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.settings.text_color, 
                self.settings.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.settings.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)