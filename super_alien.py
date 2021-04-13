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
from alien import ALien


class SuperALien(ALien):
    """A class to represent a super alien in the fleet"""

    def __init__(self, ai_game):
        """Initialize the super alien and sets its starting position"""
        super().__init__(ai_game)

        # Alien type
        self.type = "super"

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load("images/super_alien.bmp")

        # Set the life of the super alien
        self.life = self.settings.super_alien_life
