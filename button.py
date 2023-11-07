import pygame.font


class Button:
    def __init__(self, ai_game, msg):
        """Initialisation of button attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Defining the dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Create a button rectangle and centre it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The message displayed by the button
        self._prep_msg(msg)
    
    def _prep_msg(self, msg):
        """Positioning of the communicate and centred text on the button"""
        self.mgs_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.mgs_image_rect = self.mgs_image.get_rect()
        self.mgs_image_rect.center = self.rect.center

    def draw_button(self):
        # Displaying an empty button followed by a message on it
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.mgs_image, self.mgs_image_rect)
