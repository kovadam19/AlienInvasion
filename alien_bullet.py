##################################################
# Project: Alien Invasion
# Author: Adam Kovacs
# Version: 1.0.0
# Maintainer: Adam Kovacs
# E-mail: kovadam19@gmail.com
# Released: 13 April 2021
##################################################

# Generic/Built-in imports
import pygame
from pygame.sprite import Sprite


class AlienBullet(Sprite):
    """A class to manage alien bullets fired from the queen alien"""

    def __init__(self, ai_game):
        """Create a bullet object at the queen's current position"""
        # Initialise the sprite and get game screen & settings
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.queen_bullet_color

        # Create a bullet rect at (0, 0) and then set the correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)

        for alien in ai_game.aliens.sprites():
            if alien.type == "queen":
                self.rect.midbottom = alien.rect.midbottom

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen"""
        # Update the decimal position of the bullet
        self.y += self.settings.queen_bullet_speed

        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
