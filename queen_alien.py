import pygame
from alien import ALien


class QueenALien(ALien):
    """A class to represent a queen alien in the fleet"""

    def __init__(self, ai_game):
        """Initialize the queen alien and sets its starting position"""
        super().__init__(ai_game)

        # Alien type
        self.type = "queen"

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load("images/queen_alien.bmp")

        # Set the life of the queen alien
        self.life = 15