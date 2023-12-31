import sys
from time import sleep

import pygame

# initialisation of files
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """A general class designed to manage resources and the way the game works"""

    def __init__(self):
        """Initialisation of the game and creation of its resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')

        # Create an instance to store game statistics and a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Creation of a missile group
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        # Make the play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start of the main game loop"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Response to mouse and keyboard events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                    
    def _check_play_button(self, mouse_pos):
        """Starting a new game when the user clicks a button"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:

            # Resetting the game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Removal of aliens and bullets from the list
            self.aliens.empty()
            self.bullets.empty()

            # Creation of a new fleet and centring of the ship
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Keystroke response"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Response to key release"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Creating a new missile and adding it to a group of missiles"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Updating the position of buttons and susceptibility of those not visible on the screen"""
        # Updating the position of the keys
        self.bullets.update()

        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Response to collisions between missile and alien"""
        # Removal of all projectiles and foreign objects between which there has been a collision
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Level number incrementation
            self.stats.level += 1 
            self.sb.prep_level()

    def _update_aliens(self):
        """Check if the fleet is at an edge,then update the positions of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # Collision detection between alien and ship
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Checking whether any aliens have reached the bottom edge of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Just as in the case of a ship incident with aliens
                self._ship_hit()
                break

    def _ship_hit(self):
        """Reaction to the impact of the alien on the ship"""
        # Reduction of the value stored in ships_left
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Deletion of contents of aliens and bullets lists
            self.aliens.empty()
            self.bullets.empty()

            # Creation of a new fleet and centring of the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            # Starting the game in the active state
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Creation of a full foreign fleet"""
        # Creation of a foreign
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determining how many alien rows will fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Creation of a full foreign fleet
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Creating an alien and placing it in a row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Appropriate reaction when a stranger reaches the edge of the screen"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Move the entire alien fleet down and change the direction in which it moves"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_color) 
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Display of scoring information
        self.sb.show_score()

        # Display of the button only when the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()

