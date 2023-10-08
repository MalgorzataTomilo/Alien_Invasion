import pygame.font

class Scoreboard:
    '''Klasa przeznaczona do przedstawiania informacji o punktacji'''
    def __init__(self, ai_game):
        '''Inicjalizacja strybutów dotyczących punktacji'''
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        # ustawienia czcionki dla informacji dotyczących punktacji 
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # przygotowywanie początkowych obrazów z punktacją
        self.prep_score()
        self.prep_high_score()
        
    def prep_score(self):
        '''Przekształcenie punktacji na wygenerowany obraz'''
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        # Wyświetlenie punktacji w prawym górnym rogu ekranu
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20 
        self.score_rect.top = 20
        
    def show_score(self):
        '''Wyświetlanie punktacji na ekranie'''
        self.screen.blit(self.score_image, self.score_rect)

    def prep_high_score(self):
        '''Konwersja najlepszego wyniku w grze na wygenerowany obraz'''
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.hegh_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        #Wyświetlenie najlepszego wyniku w grze na środku ekranu 
        self.high_score_rect = self.hegh_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top