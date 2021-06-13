import pygame.font
from pygame.sprite import Sprite
from settings import Settings

class Square(Sprite):
    import pygame.font

    def __init__(self, game, row, col):
        super().__init__()
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.row, self.col = row, col
        self.display_number = game.unsolved[row][col]
        self.number = game.solved[row][col]
        
        self.editable = not bool(self.display_number)
        self.selected = False
        self.annotations = [False]*10
        self.highlight = self.settings.button_highlight

        self.width = self.height = self.settings.square_size
        self.font = pygame.font.SysFont(None, 48)
        self.smaller_font = pygame.font.SysFont(None, 24)

        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.border_rect = pygame.Rect(0,0,self.width+12,self.height+12)
        self.rect.top = self.settings.grid_spacing * (self.row + 1) + self.row * self.settings.square_size
        self.rect.left = self.settings.grid_spacing * (self.col + 1) + self.col * self.settings.square_size
        self.border_rect.center = self.rect.center
        
        self._update_number(str(self.display_number))
        self._add_annotations(0)



    def _update_number(self, number):
        self.display_number = number
        if self.display_number == "0":
            self.display_number = ""
        self.msg_image = self.font.render(self.display_number, True, self.settings.text_color, 
                self.settings.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_square(self):
        if self.selected:
            self.screen.fill(self.highlight, self.border_rect)
        self.screen.fill(self.settings.button_color, self.rect)
        
        for i in range(1,10):
            if self.annotations[i]:
                self.screen.blit(self.annotations_images[i], self.annotations_images_rect[i])

        if self.display_number != "":
            self.screen.blit(self.msg_image, self.msg_image_rect)

    def _is_selected(self):
        self.selected = True

    def _is_deselected(self):
        self.selected = False

    def _add_annotations(self, number):
        if number == 0:
            return
        else:
            self.annotations[number] = True
        self.annotations_images = [self.smaller_font.render(str(i), True, self.settings.text_color, self.settings.button_color) 
        if self.annotations[i] else False for i in range(0, 10)]
        self.annotations_images_rect = [i.get_rect() if i else False for i in self.annotations_images]
        for i in range(1,10):
            if self.annotations_images_rect[i]:
                self.annotations_images_rect[i].center = self.rect.center
                if i == 1 or i == 4 or i == 7:
                    self.annotations_images_rect[i].left = self.rect.left
                if i == 3 or i == 6 or i == 9:
                    self.annotations_images_rect[i].right = self.rect.right
                if i == 1 or i == 2 or i == 3:
                    self.annotations_images_rect[i].top = self.rect.top
                if i == 7 or i == 8 or i == 9:
                    self.annotations_images_rect[i].bottom = self.rect.bottom

    def _annotate(self):
        self.highlight = self.settings.button_highlight_2

    def _deannotate(self):
        self.highlight = self.settings.button_highlight
