import sys
import pygame
from time import sleep
from random import random

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import ALien
from super_alien import SuperALien


class AlienInvasion:
    """Overall class to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion by Adam")

        # Create an instance to store game statistics and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Respond to key and mouse events"""
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

    def _check_keydown_events(self, event):
        """Respond to key presses"""
        # Move the ship to the right
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        # Move the ship to the left
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        # Move the ship up
        if event.key == pygame.K_UP:
            self.ship.moving_up = True

        # Move the ship down
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = True

        # Firing bullet
        if event.key == pygame.K_SPACE:
            self._fire_bullet()

        # Quit by key q
        if event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        # Stop moving the ship right
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

        # Stop moving the ship left
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

        # Stop moving the ship up
        if event.key == pygame.K_UP:
            self.ship.moving_up = False

        # Stop moving the ship down
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.stats.game_active:
            # Reset game settings
            self.settings.initialize_dynamic_settings()

            # Reset game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self.ship.center_ship()
            self._create_fleet()

            # Hide mouse cursor
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and delete the old ones"""
        # Update bullet position
        self.bullets.update()

        # Delete bullets that reached the top of the screen
        for bullet in self.bullets.sprites():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        # Check for any bullets that have hit a simple alien
        # If so, get rid of the bullet and the alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, False)

        # Check if there is any alien collision
        if collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    # Decrease the life of the alien
                    alien.life -= 1
                    # Check if the alien is a simple one and it is destroyed
                    if alien.life == 0 and alien.type == "simple":
                        # There is a chance for a simple alien to become a super alien
                        if random() <= self.settings.super_alien_chance:
                            # Create a new super alien
                            new_super_alien = SuperALien(self)
                            # Get the position of the simple alien
                            new_super_alien.x = alien.x
                            new_super_alien.rect.x = alien.rect.x
                            new_super_alien.rect.y = alien.rect.y
                            # Add the super alien to the fleet
                            self.aliens.add(new_super_alien)
                        # Remove the simple alien
                        self.aliens.remove(alien)
                        # Increase the score
                        self.stats.score += self.settings.alien_points
                    # Check if the alien is a super one and it is destroyed
                    elif alien.life == 0 and alien.type == "super":
                        # Remove super alien
                        self.aliens.remove(alien)
                        # Increase the score
                        self.stats.score += self.settings.super_alien_points

            # Prep score and check high score
            self.sb.prep_score()
            self.sb.check_high_score()

            # Give an extra bullet after each 5000 points
            if self.stats.score != 0 and self.stats.score % 5000 == 0:
                self.settings.bullets_allowed += 1

        # Check if the fleet is empty
        if not self.aliens:
            # Center the ship
            self.ship.center_ship()

            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase the number of destroyed fleet
            self.stats.destroyed_fleets += 1

            if self.stats.destroyed_fleets % 2 == 0:
                self.settings.bullet_speed *= self.settings.speedup_scale

            # Increase the level
            self.stats.level += 1
            self.sb.prep_level()

            # Pause
            sleep(0.5)

    def _update_aliens(self):
        """Check if fleet is at an edge and update the positions of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Create an alien and find the number of aliens in a row
        # Spacing between each alien is equal to one alien width
        alien = ALien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create first row of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create a single alien for the fleet"""
        # Create an alien and place it in the row
        alien = ALien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        # Check for aliens
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop entire fleet and change the fleet's direction"""
        # Check for aliens
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        # Change the direction
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            # Decrement ships left, update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of the any remaining aliens or bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()

        # Check the aliens
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this same as if the ship got hit
                self._ship_hit()
                break

    def _update_screen(self):
        """Update images on the screen and flip to the new screen"""
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # Draw score information
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
