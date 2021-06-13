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

        self.color = self.settings.button_color

        self.width = self.height = self.settings.square_size
        self.font = pygame.font.SysFont(None, 48)
        self.smaller_font = pygame.font.SysFont(None, 24)

        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.top = (2 * self.settings.grid_spacing + (self.row + self.row // 3) * 
            self.settings.grid_spacing + self.row * self.settings.square_size)
        self.rect.left = (2 * self.settings.grid_spacing + (self.col + self.col // 3) * 
            self.settings.grid_spacing + self.col * self.settings.square_size)
        
        self._update_number(str(self.display_number))
        self._add_annotations(0)



    def _update_number(self, number):
        self.display_number = number
        if self.display_number == "0":
            self.display_number = ""
        self.msg_image = self.font.render(self.display_number, True, self.settings.text_color, 
                self.color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_square(self):
        self.screen.fill(self.color, self.rect)
        
        for i in range(1,10):
            if self.annotations[i]:
                self.screen.blit(self.annotations_images[i], self.annotations_images_rect[i])

        if self.display_number != "":
            self.screen.blit(self.msg_image, self.msg_image_rect)

    def _is_selected(self):
        self.selected = True
        self.color = self.settings.button_selected
        self._update_number(self.display_number)
        self._add_annotations(0)

    def _is_deselected(self):
        self.selected = False
        self.color = self.settings.button_color
        self._update_number(self.display_number)
        self._add_annotations(0)

    def _add_annotations(self, number):
        """Pass 0 to this function to update annotation colors"""
        if number != 0:
            self.annotations[number] = True
        self.annotations_images = [self.smaller_font.render(str(i), True, self.settings.text_color, self.color) 
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

    def _highlight_right_click(self):
        self.color = self.settings.button_highlight_2
        self._add_annotations(0)
        self._update_number(self.display_number)

    def _remove_highlight_right_click(self):
        self.color = self.settings.button_selected
        self._add_annotations(0)
        self._update_number(self.display_number)

    def _deannotate(self):
        self.annotations = [False]*10
        
    def _remove_one_annotation(self):
        for i in range(0, 10):
            if self.annotations[9-i]:
                self.annotations[9-i] = False
                return