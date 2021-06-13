class Settings:
    """A class to store all settings for alien invasion"""
    def __init__(self):
        """Initialize the game settings"""
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)
        self.button_selected = (255,255,0)
        self.button_color = (200,200,200)
        self.text_color = (0,0,0)
        self.button_highlight = (100,100,100)
        self.button_highlight_2 = (50, 150, 150)
        self.grid_spacing = min(self.screen_width, self.screen_height) // 30
        self.square_size = min(self.screen_width, self.screen_height) // 10