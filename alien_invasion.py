import sys
import pygame
from settings import Settings
from ship import Ship

class AlienInvasion:
    '''Ogólna klasa przeznaczona do zarządzania zasobami i sposobem działania gry'''

    def __init__(self):
        '''Inicjalizacja gry i utworzenie jej zasobów'''
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Inwacja Obcych')
        self.ship = Ship(self)


    def run_game(self):
        '''Rozpoczęcie pętli głównej gry'''
        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        pygame.display.flip()
         

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()