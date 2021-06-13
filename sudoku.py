import sys
from time import sleep
import pygame
from remover import main
from settings import Settings
from square import Square
from button import Button
from button import SmallerButton


class Sudoku:
    """Overall class to manage game assests and behavior"""

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0,0), (pygame.FULLSCREEN))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.settings.grid_spacing = min(self.settings.screen_width, self.settings.screen_height) // 50
        self.settings.square_size = min(self.settings.screen_width, self.settings.screen_height) // 12
        pygame.display.set_caption("Sudoku")

        self.keys = [
            pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9
        ]
        self.difficulty = 0
        self.difficulties = ["Baby", "Novice", "Easy", "Normal", "Hard", "Expert", "Evil"]

        self.new_game()

    def new_game(self):
        self.solved, self.unsolved = main(self.difficulty)

        self.squares = [
        [0] * 9,
        [0] * 9,
        [0] * 9,
        [0] * 9,
        [0] * 9,
        [0] * 9,
        [0] * 9,
        [0] * 9,
        [0] * 9,
        ]

        self.selected_square = None
        self.annotating = False

        self._create_grid()
        self._create_buttons()


    def run_game(self):
        while True:
            self._check_events()

            self._update_screen()

    def _check_events(self):
        #Watch for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_squares(mouse_pos, event)
                self._check_buttons(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            

    def _check_buttons(self, mouse_pos):
        self._check_solution(mouse_pos)
        if self.button_reset.rect.collidepoint(mouse_pos):
            self._reset_solution()
        elif self.button_reset_square.rect.collidepoint(mouse_pos):
            self._reset_square(self.selected_square)
        elif self.button_reveal.rect.collidepoint(mouse_pos):
            self._reveal_solution()
        elif self.button_reveal_square.rect.collidepoint(mouse_pos):
            self._reveal_square(self.selected_square)
        elif self.button_difficulty_lower.rect.collidepoint(mouse_pos):
            self._update_difficulty(-1)
        elif self.button_difficulty_raise.rect.collidepoint(mouse_pos):
            self._update_difficulty(1)
        elif self.button_new.rect.collidepoint(mouse_pos):
            self.new_game()

    def _check_squares(self, mouse_pos, event):
        for row in self.squares:
            for square in row:
                if square.rect.collidepoint(mouse_pos):
                    old_annotated = self.annotating
                    new_annotated = True if event.button == 3 else False                    
                    self._change_selected_square(self.selected_square, square, old_annotated, new_annotated)
                    return

    def _change_selected_square(self, old_square, new_square, old_annotated, new_annotated):
        if old_square == new_square:
            if old_annotated != new_annotated:
                if old_annotated == True:
                    self._mark_deannotated()
                else:
                    self._mark_annotated()
            else:
                self.selected_square._is_deselected()
                self.selected_square = None
            return
        if old_annotated:
            self._mark_deannotated()
        if old_square:
            old_square._is_deselected()
        self.selected_square = new_square
        self.selected_square._is_selected()
        if new_annotated:
            self._mark_annotated()


    def _check_keydown_events(self, event):
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key in self.keys:
            if self.selected_square and self.selected_square.editable:
                if not self.annotating:
                    self._remove_all_annotations()
                    self.selected_square._update_number(str(self.keys.index(event.key)))
                else:
                    self.selected_square._update_number(str(0))
                    self.selected_square._add_annotations(self.keys.index(event.key))
        elif event.key == pygame.K_UP:
            if self.selected_square:
                row = (self.selected_square.row + 8) % 9
                col = self.selected_square.col
                self._change_selected_square(self.selected_square, self.squares[row][col], self.annotating, False)
        elif event.key == pygame.K_DOWN:
            if self.selected_square:
                row = (self.selected_square.row + 1) % 9
                col = self.selected_square.col
                self._change_selected_square(self.selected_square, self.squares[row][col], self.annotating, False)
        elif event.key == pygame.K_LEFT:
            if self.selected_square:
                row = self.selected_square.row
                col = (self.selected_square.col + 8) % 9
                self._change_selected_square(self.selected_square, self.squares[row][col], self.annotating, False)
        elif event.key == pygame.K_RIGHT:
            if self.selected_square:
                row = self.selected_square.row
                col = (self.selected_square.col + 1) % 9
                self._change_selected_square(self.selected_square, self.squares[row][col], self.annotating, False)
        elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
            if self.selected_square and self.selected_square.editable:
                if not self.annotating:
                    self.selected_square._update_number(str(0))
                else:
                    self.selected_square._remove_one_annotation()
        elif event.key == pygame.K_SPACE:
            self._change_selected_square(self.selected_square, self.selected_square, self.annotating, not self.annotating)


    def _check_keyup_events(self, event):
        pass

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for row in self.squares:
            for square in row:
                square.draw_square()
        for button in self.buttons:
            button.draw_button()
        pygame.display.flip()

    def _create_grid(self):
        for i in range(9):
            for j in range(9):
                self.squares[i][j] = Square(self, i, j)

    def _create_buttons(self):
        self.button_reset = Button(self)
        self.button_reset.rect.bottom = self.squares[8][8].rect.bottom
        self.button_reset.rect.left = self.squares[8][8].rect.right + 2 * self.settings.grid_spacing
        self.button_reset._prep_msg("Reset grid")


        self.button_reset_square = Button(self)
        self.button_reset_square.rect.bottom = self.button_reset.rect.top - self.settings.grid_spacing
        self.button_reset_square.rect.left = self.button_reset.rect.left
        self.button_reset_square._prep_msg("Reset current")

        self.button_check = Button(self)
        self.button_check.rect.bottom = self.button_reset_square.rect.top - self.settings.grid_spacing
        self.button_check.rect.left = self.button_reset.rect.left
        self.button_check._prep_msg("Check solution")

        self.button_new = Button(self)
        self.button_new.rect.bottom = self.button_check.rect.top - self.settings.grid_spacing
        self.button_new.rect.left = self.button_check.rect.left
        self.button_new._prep_msg("New game")

        self.button_reveal = Button(self)
        self.button_reveal.rect.bottom = self.button_reset.rect.bottom
        self.button_reveal.rect.left = self.button_reset.rect.right + self.settings.grid_spacing
        self.button_reveal._prep_msg("Reveal solution")

        self.button_reveal_square = Button(self)
        self.button_reveal_square.rect.bottom = self.button_reveal.rect.top - self.settings.grid_spacing
        self.button_reveal_square.rect.left = self.button_reveal.rect.left
        self.button_reveal_square._prep_msg("Reveal current")

        self.button_difficulty_lower = SmallerButton(self)
        self.button_difficulty_lower.rect.bottom = self.button_reveal_square.rect.top - self.settings.grid_spacing
        self.button_difficulty_lower.rect.left = self.button_reveal.rect.left
        self.button_difficulty_lower._prep_msg("-")

        self.button_difficulty_raise = SmallerButton(self)
        self.button_difficulty_raise.rect.bottom = self.button_difficulty_lower.rect.bottom
        self.button_difficulty_raise.rect.right = self.button_reveal.rect.right
        self.button_difficulty_raise._prep_msg("+")

        self.button_difficulty = Button(self)
        self.button_difficulty.rect.bottom = self.button_difficulty_lower.rect.top - self.settings.grid_spacing
        self.button_difficulty.rect.left = self.button_reveal.rect.left
        self.button_difficulty._prep_msg(f"Difficulty: {self.difficulties[self.difficulty]}")

        self.buttons = [self.button_new, self.button_reset, self.button_reset_square, self.button_reveal, self.button_reveal_square, 
        self.button_check, self.button_difficulty_raise, self.button_difficulty_lower, self.button_difficulty]

    def _check_solution(self, mouse_pos):
        if self.button_check.clicked:
            self.button_check.clicked = False
            self.button_check._prep_msg("Check solution")
        if not self.button_check.rect.collidepoint(mouse_pos):
            return
        self.button_check.clicked = True
        mistakes = 0
        filled = 0
        for row in self.squares:
            for square in row:
                if square.display_number != "":
                    filled += 1
                    if square.display_number != str(square.number):
                        mistakes += 1
        if filled == 81 and mistakes == 0:
            self.button_check._prep_msg("Solved!")
        else:
            self.button_check._prep_msg(f"{mistakes} mistakes")
        
    def _reveal_solution(self):
        for row in self.squares:
            for square in row:
                self._reveal_square(square)

    def _reveal_square(self, square):
        if square:
            square._deannotate()
            square._update_number(str(square.number))

    def _reset_square(self, square):
        if square and square.editable:
            square._deannotate()
            square._update_number("0")
    
    def _reset_solution(self):
        for row in self.squares:
            for square in row:
                self._reset_square(square)

    def _update_difficulty(self, number):
        if number == 1:
            if self.difficulty + number > 6:
                return
            else: self.difficulty += 1
        elif number == -1:
            if self.difficulty + number < 0:
                return
            else: self.difficulty -= 1
        self.button_difficulty._prep_msg(f"Difficulty: {self.difficulties[self.difficulty]}")

    def _mark_annotated(self):
        if self.selected_square and self.selected_square.editable:
            self.annotating = True
            self.selected_square._highlight_right_click()
            
    
    def _mark_deannotated(self):
        if self.selected_square:
            self.annotating = False
            self.selected_square._remove_highlight_right_click()

    def _remove_all_annotations(self):
       if self.selected_square:
           self.selected_square._deannotate()











if __name__ == '__main__':
    game = Sudoku()
    game.run_game()